from typing import Optional, Union

from database.dal.sql.synchronous import DataAccessLayer
from database.types import ID, CreateType, ModelType, SchemaType, UpdateType
from lib.password import get_password_hash, verify_password
from lib.utilities import logger
from models.users import Users, UsersSchema, UsersSchemaCreate, UsersSchemaUpdate
from sqlalchemy import select
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

UserModelType = Union[Users, ModelType]
UserSchemaType = Union[UsersSchema, SchemaType]
UserCreateType = Union[UsersSchemaCreate, CreateType]
UserUpdateType = Union[UsersSchemaUpdate, UpdateType]


class UserDal(DataAccessLayer):
    def __init__(self, model: UserModelType = Users, max_limit: ID = 1000):
        super().__init__(model, max_limit)

    def get_by_name(self, db: Session, username: str) -> Optional[Users]:
        with db as session:
            try:
                statement = select(self.model).filter_by(username=username)
                data = session.scalars(statement).one_or_none()
            except DataError as e:
                logger.warning("%s - %s", e.__class__.__name__, e)
                return None
        return data

    def create(self, db: Session, data: CreateType) -> Users:
        hashed_password = get_password_hash(data.get("password", "changeME"))
        data["password"] = hashed_password
        return super().create(db, data)

    def update(self, db: Session, id: ID, data: UpdateType) -> Users:
        hashed_password = get_password_hash(data.get("password", "changeME"))
        data["password"] = hashed_password
        return super().update(db, id, data)

    def change_password(self, db: Session, name: str, new_password: str) -> None:
        user = self.get_by_name(db, name)
        user.password = new_password
        data = user.as_dict()
        id = data.pop("id")
        self.update(db, id, data)

    def authenticate(self, db: Session, name: str, password: str) -> Optional[Users]:
        if not (user := self.get_by_name(db, name)):
            return None
        hashed_password = user.password
        if not verify_password(password, hashed_password):
            return None
        return user

    def is_active(self, user: UserSchemaType) -> bool:
        return user.is_active

    def is_superuser(self, user: UserSchemaType) -> bool:
        return user.is_superuser
