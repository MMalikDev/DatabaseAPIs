from typing import Any, Dict, List, Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId
from configs.core import settings
from database import Base
from lib.utilities import logger
from pymongo import MongoClient

ObjectID = str
ModelType = Base
CreateType = Dict[str, Any]
UpdateType = Dict[str, Any]
Query = Dict[str, str]


class DataAccessLayer:
    def __init__(self, name: str, max_limit: int = 1000) -> None:
        self.name: str = name
        self.max_limit = max_limit

        client = MongoClient(settings.NOSQL_URI)
        database = client["test"]
        self.db = database[self.name]

    def read_all(self, query: Query = {}, limit: int = 1000) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        items = self.db.find(query).limit(limit)
        result = []
        for item in items:
            item["_id"] = str(item["_id"])
            result.append(item)
        return result

    def create(self, data: CreateType) -> Optional[ModelType]:
        result = self.db.insert_one(data)
        return self.read_1(result.inserted_id)

    def read_1(self, id: ObjectID) -> Optional[ModelType]:
        if not (_id := self.get_id(id)):
            return None
        item = self.db.find_one({"_id": _id})
        item["_id"] = str(item["_id"])
        return item

    def update(self, id: ObjectID, data: UpdateType) -> Optional[ModelType]:
        if not (_id := self.get_id(id)):
            return None
        data = self.db.update_one({"_id": _id}, {"$set": data})
        return self.read_1(id)

    def delete(self, id: ObjectID) -> bool:
        if not (_id := self.get_id(id)):
            return False
        if not (data := self.db.delete_one({"_id": _id})):
            return False
        return data.deleted_count == 1

    @staticmethod
    def get_id(id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(id)
        except InvalidId as e:
            logger.debug("%s - %s", e.__class__.__name__, e)
            return None
