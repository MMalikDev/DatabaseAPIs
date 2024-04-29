from database import Base
from faker import Faker
from sqlalchemy import Column, Integer, String


class Images(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    author: str = Column(String)
    description: str = Column(String)
    download_url: str = Column(String)


class Image:
    def __init__(self, *args, **kwargs) -> None:

        fake = Faker()

        self.author = fake.name()
        self.download_url = fake.ssn()
        self.description = fake.paragraph(nb_sentences=5)
