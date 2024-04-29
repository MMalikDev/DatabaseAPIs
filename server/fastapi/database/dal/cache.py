import json
from typing import List, Optional

from database import cache
from database.cache import cache
from database.types import ID, ModelType, SessionType, UpdateType
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .base import DataAccessLayerBase


class CacheAccessLayerBase:
    model: ModelType
    cache: Redis

    def get_key(self, *args, id: ID, **kwargs) -> str:
        key = f"{self.model.__name__} {args} {kwargs} {id}"
        # Hash Key for more Anonymity
        return key

    def clear_cached(self, *args, id: ID, **kwargs) -> None:
        key = self.get_key(*args, id=id, **kwargs)
        if self.cache.exists(key):
            self.cache.delete(key)


class CacheAccessLayerSync(DataAccessLayerBase, CacheAccessLayerBase):
    def __init__(self, model: ModelType, cache_exp: int = 60, max_limit: int = 1000):
        super().__init__(model, max_limit=max_limit)
        self.cache = cache
        self.cache_exp = cache_exp

    def read_all(
        self, db: SessionType, page: int = 1, limit: int = 100
    ) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        key = self.get_key(page, limit, id="LIST")

        if cache := self.cache.get(key):
            return [self.model(**i) for i in json.loads(cache)]

        data = super().read_all(db, page, limit)
        self.cache.set(key, json.dumps([i.as_dict() for i in data]), self.cache_exp)
        return data

    def read_1(self, db: SessionType, id: ID) -> Optional[ModelType]:
        key = self.get_key(id=id)

        if cache := self.cache.get(key):
            return self.model(**json.loads(cache))

        if not (data := super().read_1(db, id)):
            return None

        self.cache.set(key, json.dumps(data.as_dict()), self.cache_exp)
        return data

    def update(self, db: SessionType, id: ID, data: UpdateType) -> Optional[ModelType]:
        if not (model := super().update(db, id, data)):
            return None
        self.clear_cached(id=id)
        return model

    def delete(self, db: SessionType, id: ID) -> bool:
        if not super().delete(db, id):
            return False
        self.clear_cached(id=id)
        return True


class CacheAccessLayerAsync(DataAccessLayerBase, CacheAccessLayerBase):
    def __init__(self, model: ModelType, cache_exp: int = 60, max_limit: int = 1000):
        super().__init__(model, max_limit)
        self.cache = cache
        self.cache_exp = cache_exp

    async def read_all(
        self, db: SessionType, page: int = 1, limit: int = 100
    ) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        key = self.get_key(page, limit, id="LIST")

        if cache := self.cache.get(key):
            return [self.model(**i) for i in json.loads(cache)]

        data = await super().read_all(db, page, limit)
        self.cache.set(key, json.dumps([i.as_dict() for i in data]), self.cache_exp)
        return data

    async def read_1(self, db: SessionType, id: ID) -> Optional[ModelType]:
        key = self.get_key(id=id)

        if cache := self.cache.get(key):
            return self.model(**json.loads(cache))

        if not (data := await super().read_1(db, id)):
            return None

        self.cache.set(key, json.dumps(data.as_dict()), self.cache_exp)
        return data

    async def update(
        self, db: SessionType, id: ID, data: UpdateType
    ) -> Optional[ModelType]:
        if not (item := await super().update(db, id, data)):
            return None
        self.clear_cached(id=id)
        return item

    async def delete(self, db: SessionType, id: ID) -> bool:
        if not await super().delete(db, id):
            return False
        self.clear_cached(id=id)
        return True
