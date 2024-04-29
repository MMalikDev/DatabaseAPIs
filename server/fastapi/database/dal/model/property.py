from typing import List, Union

from database import Base
from database.dal.sql.synchronous import DataAccessLayer
from database.types import ID, CreateType, ModelType
from models.property import Property
from sqlalchemy.orm import Session

PropertyModelType = Union[Property, ModelType]


class PropertyDal(DataAccessLayer):
    def __init__(self, model: Base = Property, max_limit: ID = 1000):
        super().__init__(model, max_limit)

    def create_with_owner(
        self, db: Session, data: CreateType, owner_id: int
    ) -> PropertyModelType:
        data["owner_id"] = owner_id
        return super().create(db, data)

    def list_by_owner(
        self, db: Session, owner_id: int, page: int = 1, limit: int = 100
    ) -> List[PropertyModelType]:
        limit = min(limit, self.max_limit)
        offset = (page - 1) * limit
        with db as session:
            data = (
                session.query(self.model)
                .filter(self.model.owner_id == owner_id)
                .offset(offset)
                .limit(limit)
                .all()
            )
        return data
