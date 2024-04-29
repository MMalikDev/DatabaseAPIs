from abc import ABC, abstractmethod

from fastapi import APIRouter


class BaseController(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.router = APIRouter()
        self.descriptions = self._PathDescription(self.name)

    class _PathDescription:
        def __init__(self, name) -> None:
            self.LIST = f"List all {name}"

            self.CREATE = f"Create a new {name}"
            self.READ = f"Get a {name}"
            self.UPDATE = f"Update a {name}"
            self.DELETE = f"Delete a {name}"

    def _404_detail(self, id) -> str:
        return f"{self.name} with ID {id} not found"

    def pagination(self, data: list, page: int = 1, limit: int = 100) -> list:
        startIndex = (page - 1) * limit
        endIndex = page * limit

        data = data[startIndex:endIndex]
        return data

    # Base Configuration
    def add_default_endpoints(self) -> None:
        self.add_list_endpoint()
        self.add_create_endpoint()
        self.add_read_endpoint()
        self.add_update_endpoint()
        self.add_delete_endpoint()

    @abstractmethod
    def add_list_endpoint():
        pass

    @abstractmethod
    def add_create_endpoint():
        pass

    @abstractmethod
    def add_read_endpoint():
        pass

    @abstractmethod
    def add_update_endpoint():
        pass

    @abstractmethod
    def add_delete_endpoint():
        pass
