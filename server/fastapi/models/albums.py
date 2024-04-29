from typing import TYPE_CHECKING, Optional

from database import Base
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from models.artists import Artist
    from models.songs import Song


class Album(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    title: str = Column(String)

    song_id: Optional[int] = Column(Integer, ForeignKey("song.id"), nullable=True)
    artist_id: Optional[int] = Column(Integer, ForeignKey("artist.id"), nullable=True)

    songs = relationship("Song", foreign_keys=[song_id])
    artists = relationship("Artist", foreign_keys=[artist_id])


class AlbumSchema(BaseModel):
    id: int
    title: str

    song_id: Optional[int]
    artist_id: Optional[int]


class AlbumSchemaCreate(BaseModel):
    title: str

    song_id: Optional[int]
    artist_id: Optional[int]


class AlbumSchemaUpdate(BaseModel):
    title: str

    song_id: Optional[int]
    artist_id: Optional[int]
