from typing import TYPE_CHECKING, Optional

from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.albums import Album


class Artist(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    first_name: str = Column(String)
    last_name: str = Column(String)
    nationality: str = Column(String)

    album_id: Optional[int] = Column(Integer, ForeignKey("album.id"), nullable=True)
    albums = relationship("Album", foreign_keys=[album_id])


class ArtistSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    nationality: str

    album_id: Optional[int]


class ArtistSchemaCreate(BaseModel):
    first_name: str
    last_name: str
    nationality: str

    album_id: Optional[int]


class ArtistSchemaUpdate(BaseModel):
    first_name: str
    last_name: str
    nationality: str

    album_id: Optional[int]
