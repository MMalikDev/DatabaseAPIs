from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(alias="_id")
    title: str
    author: str
    synopsis: str


class BookCreate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]
