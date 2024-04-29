from database import Base
from faker import Faker
from sqlalchemy import Boolean, Column, Integer, String


class Users(Base):
    id: int = Column(Integer, primary_key=True, index=True)

    # email: str = Column(String, unique=True, nullable=False)

    username: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)

    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)


class User:
    def __init__(self, *args, **kwargs) -> None:

        fake = Faker()

        # # self.email: str = fake.email()
        self.username: str = fake.name()
        self.password: str = fake.bs().replace(" ", "")
        self.is_active = fake.boolean()
        self.is_superuser = fake.boolean()
