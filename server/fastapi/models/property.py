from typing import TYPE_CHECKING

from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.users import Users


class Property(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    name: str = Column(String, nullable=False)
    value: float = Column(Float, default=0.0)

    owner_id: str = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("Users", foreign_keys=[owner_id])


class PropertySchema(BaseModel):
    id: int
    name: str
    value: float
    owner_id: str


class PropertySchemaCreate(BaseModel):
    name: str
    value: float


class PropertySchemaUpdate(BaseModel):
    name: str
    value: float
