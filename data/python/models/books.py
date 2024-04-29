from database import Base
from faker import Faker
from sqlalchemy import Column, Integer, String


class Books(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    title: str = Column(String)
    author: str = Column(String)
    synopsis: str = Column(String)


class Book:
    def __init__(self, *args, **kwargs) -> None:

        fake = Faker()

        self.title = fake.catch_phrase()
        self.author = fake.name()
        self.synopsis = fake.paragraph(nb_sentences=3)
