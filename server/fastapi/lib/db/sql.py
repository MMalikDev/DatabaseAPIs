from typing import Any, Dict, List, Optional, Type

from configs.core import settings
from database import Base
from lib.utilities import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

ID = int
ModelType = Base
CreateType = Dict[str, Any]
UpdateType = Dict[str, Any]


class DataAccessLayer:
    def __init__(self, model: Type[ModelType], max_limit: int = 1000):
        self.model = model
        self.max_limit = max_limit

        self.engine = create_engine(settings.SQL_URI)
        self.db = Session(bind=self.engine)

        self.init_db()

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def read_all(self, page: int = 1, limit: int = 100) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        offset = (page - 1) * limit
        with self.db as session:
            data = session.query(self.model).offset(offset).limit(limit).all()
        return data

    def create(self, data: CreateType) -> ModelType:
        model = self.model(**data)
        with self.db as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return model

    def read_1(self, id: ID) -> Optional[ModelType]:
        with self.db as session:
            try:
                data = session.get(self.model, id)
            except DataError as e:
                logger.warning("%s - %s", e.__class__.__name__, e)
                return None
        return data

    def update(self, id: ID, data: UpdateType) -> Optional[ModelType]:
        if not (model := self.read_1(id)):
            return None

        fields = model.__dict__.keys()
        for field in fields:
            if field in data:
                setattr(model, field, data[field])

        with self.db as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return model

    def delete(self, id: ID) -> bool:
        if not (data := self.read_1(id)):
            return False
        with self.db as session:
            session.delete(data)
            session.commit()
        return True
