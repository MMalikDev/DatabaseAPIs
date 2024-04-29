import json
from typing import List, Optional

from database import cache
from database.dal.base import DataAccessLayerBase
from database.dal.cache import CacheAccessLayerBase
from database.types import ID, CreateType, ModelType, UpdateType
from lib.utilities import logger
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session


class DataAccessLayer(DataAccessLayerBase):
    def __init__(self, model: ModelType, max_limit: int = 1000):
        super().__init__(max_limit)
        self.model = model

    def read_all(self, db: Session, page: int = 1, limit: int = 100) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        offset = (page - 1) * limit
        with db as session:
            data = session.query(self.model).offset(offset).limit(limit).all()
        return data

    def create(self, db: Session, data: CreateType) -> Optional[ModelType]:
        model = self.model(**data)
        try:
            with db as session:
                session.add(model)
                session.commit()
                session.refresh(model)
        except IntegrityError as e:
            logger.debug("%s", e)
            logger.warning("Already Exists: %s", e.__class__.__name__)
            return None
        return model

    def read_1(self, db: Session, id: ID) -> Optional[ModelType]:
        with db as session:
            try:
                data = session.get(self.model, id)
            except DataError as e:
                logger.debug("%s", e)
                logger.warning("Invalid ID provided: %s", e.__class__.__name__)
                return None
        return data

    def update(self, db: Session, id: ID, data: UpdateType) -> Optional[ModelType]:
        if not (model := self.read_1(db, id)):
            return None
        fields = model.__dict__.keys()
        for field in fields:
            if field in data:
                setattr(model, field, data[field])

        try:
            with db as session:
                session.add(model)
                session.commit()
                session.refresh(model)
        except IntegrityError as e:
            logger.debug("%s", e)
            logger.warning("Model's Unique Values Conflict: %s", e.__class__.__name__)
            return None
        return model

    def delete(self, db: Session, id: ID) -> bool:
        if not (data := self.read_1(db, id)):
            return False
        with db as session:
            session.delete(data)
            session.commit()
        return True


class DataAccessLayerCached(DataAccessLayer, CacheAccessLayerBase):
    def __init__(self, model: ModelType, cache_exp: int = 60, max_limit: int = 1000):
        super().__init__(model, max_limit=max_limit)
        self.cache = cache
        self.cache_exp = cache_exp

    def read_all(self, db: Session, page: int = 1, limit: int = 100) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        key = self.get_key(page, limit, id="LIST")

        if cache := self.cache.get(key):
            return [self.model(**i) for i in json.loads(cache)]

        data = super().read_all(db, page, limit)
        self.cache.set(key, json.dumps([i.as_dict() for i in data]), self.cache_exp)
        return data

    def read_1(self, db: Session, id: ID) -> Optional[ModelType]:
        key = self.get_key(id=id)

        if cache := self.cache.get(key):
            return self.model(**json.loads(cache))

        if not (data := super().read_1(db, id)):
            return None

        self.cache.set(key, json.dumps(data.as_dict()), self.cache_exp)
        return data

    def update(self, db: Session, id: ID, data: UpdateType) -> Optional[ModelType]:
        if not (model := super().update(db, id, data)):
            return None
        self.clear_cached(id=id)
        return model

    def delete(self, db: Session, id: ID) -> bool:
        if not super().delete(db, id):
            return False
        self.clear_cached(id=id)
        return True
