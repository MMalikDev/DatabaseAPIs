from abc import ABC, abstractmethod
from typing import List, Optional, Type

from database.types import ID, CreateType, ModelType, SessionType, UpdateType


class DataAccessLayerBase(ABC):
    def __init__(self, max_limit: int = 1000):
        self.max_limit = max_limit

    @abstractmethod
    def read_all(
        self, db: SessionType, page: int = 1, limit: int = 100
    ) -> List[ModelType]:
        pass

    @abstractmethod
    def create(self, db: SessionType, data: CreateType) -> ModelType:
        pass

    @abstractmethod
    def read_1(self, db: SessionType, id: ID) -> Optional[ModelType]:
        pass

    @abstractmethod
    def update(self, db: SessionType, id: ID, data: UpdateType) -> Optional[ModelType]:
        pass

    @abstractmethod
    def delete(self, db: SessionType, id: ID) -> bool:
        pass
