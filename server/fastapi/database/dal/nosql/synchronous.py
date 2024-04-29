import json
from typing import List, Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId
from configs.core import settings
from database import cache
from database.dal.base import DataAccessLayerBase
from database.dal.cache import CacheAccessLayerBase
from database.types import CreateType, ModelType, ObjectID, Query, UpdateType
from lib.utilities import logger
from pymongo import MongoClient
from pymongo.database import Database


class DataAccessLayer(DataAccessLayerBase):
    def __init__(self, name: str, max_limit: int = 1000) -> None:
        super().__init__(max_limit)

        client = MongoClient(settings.NOSQL_URI)
        database = client["test"]

        self.name: str = name
        self.db: Database = database[self.name]

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


class DataAccessLayerCached(DataAccessLayer, CacheAccessLayerBase):
    def __init__(self, name: str, cache_duration: int, max_limit: int = 1000) -> None:
        super().__init__(name, max_limit)
        self.cache = cache
        self.cache_duration: int = cache_duration

    def read_all(self, query: Query = {}, limit: int = 1000) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        key: str = f"{self.name} list: {query} limit:{limit}"

        if cache := self.cache.get(key):
            return json.loads(cache)

        if not (data := super().read_all(query, limit)):
            return []

        self.cache.set(key, json.dumps(data), self.cache_duration)
        return data

    def read_1(self, id: ObjectID) -> Optional[ModelType]:
        key: str = f"{self.name} id: {id}"

        if cache := self.cache.get(key):
            return json.loads(cache)

        if not (data := super().read_1(id)):
            return None

        self.cache.set(key, json.dumps(data), self.cache_duration)
        return data
