from typing import TYPE_CHECKING, Optional

from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.albums import Album


class Song(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    title: str = Column(String)

    album_id: Optional[int] = Column(Integer, ForeignKey("album.id"), nullable=True)
    albums = relationship("Album", foreign_keys=[album_id])


class SongSchema(BaseModel):
    id: int
    title: str

    album_id: Optional[int]


class SongSchemaCreate(BaseModel):
    title: str

    album_id: Optional[int]


class SongSchemaUpdate(BaseModel):
    title: str

    album_id: Optional[int]
