from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


class Item(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    title: str = Column(String)
    description: str = Column(String)


class ItemSchema(BaseModel):
    id: int
    title: str
    description: str


class ItemSchemaCreate(BaseModel):
    title: str
    description: str


class ItemSchemaUpdate(BaseModel):
    title: str
    description: str
