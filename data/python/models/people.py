from database import Base
from faker import Faker
from sqlalchemy import Column, Integer, String


class People(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    # Name
    ssn: str = Column(String)
    name: str = Column(String)
    phone_number: str = Column(String)

    # Work
    job: str = Column(String)
    company: str = Column(String)
    catch_phrase: str = Column(String)


class Person:
    def __init__(self) -> None:

        fake = Faker()

        # Name
        self.ssn = fake.ssn()
        self.name = fake.name()

        self.phone_number = fake.phone_number()

        # Work
        self.job = fake.job()
        self.company = fake.company()
        self.catch_phrase = fake.catch_phrase()
