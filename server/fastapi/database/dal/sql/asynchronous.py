import json
from typing import List, Optional

from database import cache
from database.dal.base import DataAccessLayerBase
from database.dal.cache import CacheAccessLayerBase
from database.types import ID, CreateType, ModelType, UpdateType
from lib.utilities import logger
from sqlalchemy import update
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class DataAccessLayer(DataAccessLayerBase):
    def __init__(self, model: ModelType, max_limit: int = 1000):
        super().__init__(max_limit)
        self.model = model

    async def read_all(
        self, db: AsyncSession, page: int = 1, limit: int = 100
    ) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        offset = (page - 1) * limit
        async with db as session:
            statement = select(self.model).offset(offset).limit(limit)
            data = await session.scalars(statement)
            data = data.all()
        return data

    async def create(self, db: AsyncSession, data: CreateType) -> Optional[ModelType]:
        model = self.model(**data)
        try:
            async with db as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
        except IntegrityError as e:
            logger.debug("%s", e)
            logger.warning("Already Exists: %s", e.__class__.__name__)
            return None
        return model

    async def read_1(self, db: AsyncSession, id: ID) -> Optional[ModelType]:
        async with db as session:
            try:
                data = await session.get(self.model, id)
            except DataError as e:
                logger.debug("%s", e)
                logger.warning("Invalid ID provided: %s", e.__class__.__name__)
                return None
        return data

    async def update(
        self, db: AsyncSession, id: ID, data: UpdateType
    ) -> Optional[ModelType]:
        try:
            statement = update(self.model).where(self.model.id == id).values(**data)
            async with db as session:
                await session.execute(statement)
                await session.commit()
        except IntegrityError as e:
            logger.debug("%s", e)
            logger.warning("Model's Unique Values Conflict: %s", e.__class__.__name__)
            return None
        return await self.read_1(db, id)

    async def delete(self, db: AsyncSession, id: ID) -> bool:
        if not (data := await self.read_1(db, id)):
            return False
        async with db as session:
            await session.delete(data)
            await session.commit()
        return True


class DataAccessLayerCached(DataAccessLayer, CacheAccessLayerBase):
    def __init__(self, model: ModelType, cache_exp: int = 60, max_limit: int = 1000):
        super().__init__(model, max_limit)
        self.cache = cache
        self.cache_exp = cache_exp

    async def read_all(
        self, db: AsyncSession, page: int = 1, limit: int = 100
    ) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        key = self.get_key(page, limit, id="LIST")

        if cache := self.cache.get(key):
            return [self.model(**i) for i in json.loads(cache)]

        data = await super().read_all(db, page, limit)
        self.cache.set(key, json.dumps([i.as_dict() for i in data]), self.cache_exp)
        return data

    async def read_1(self, db: AsyncSession, id: ID) -> Optional[ModelType]:
        key = self.get_key(id=id)

        if cache := self.cache.get(key):
            return self.model(**json.loads(cache))

        if not (data := await super().read_1(db, id)):
            return None
        self.cache.set(key, json.dumps(data.as_dict()), self.cache_exp)
        return data

    async def update(
        self, db: AsyncSession, id: ID, data: UpdateType
    ) -> Optional[ModelType]:
        if not (item := await super().update(db, id, data)):
            return None
        self.clear_cached(id=id)
        return item

    async def delete(self, db: AsyncSession, id: ID) -> bool:
        if not await super().delete(db, id):
            return False
        self.clear_cached(id=id)
        return True
