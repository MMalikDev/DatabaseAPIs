from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically

        Returns:
            str: Class name in lower case of the object that inherits from Base
        """

        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
