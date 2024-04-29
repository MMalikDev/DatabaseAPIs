from database import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, Column, Integer, String


class Users(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    # email: str = Column(String, unique=True, nullable=False)

    username: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)

    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)


class UsersSchema(BaseModel):
    id: int
    # email: EmailStr
    username: str
    password: str

    is_active: bool
    is_superuser: bool


class UsersSchemaCreate(BaseModel):
    # email: EmailStr
    username: str
    password: str

    is_active: bool = True
    is_superuser: bool = False


class UsersSchemaUpdate(BaseModel):
    # email: EmailStr
    username: str
    password: str

    is_active: bool
    is_superuser: bool
