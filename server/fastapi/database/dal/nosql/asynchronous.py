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
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class DataAccessLayer(DataAccessLayerBase):
    def __init__(self, name: str, max_limit: int = 1000) -> None:
        super().__init__(max_limit)

        client = AsyncIOMotorClient(settings.NOSQL_URI)
        database = client["admin"]

        self.name: str = name
        self.db: AsyncIOMotorDatabase = database[self.name]

    async def read_all(self, query: Query = {}, limit: int = 1000) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        items = await self.db.find(query).to_list(limit)

        result = []
        for item in items:
            item["_id"] = str(item["_id"])
            result.append(item)
        return result

    async def create(self, data: CreateType) -> Optional[ModelType]:
        result = await self.db.insert_one(data)
        return await self.read_1(result.inserted_id)

    async def read_1(self, id: ObjectID) -> Optional[ModelType]:
        if not (_id := self.get_id(id)):
            return None
        item = await self.db.find_one({"_id": _id})
        item["_id"] = str(item["_id"])
        return item

    async def update(self, id: ObjectID, data: UpdateType) -> Optional[ModelType]:
        if not (_id := self.get_id(id)):
            return None
        data = await self.db.update_one({"_id": _id}, {"$set": data})
        if data.modified_count != 1:
            return None
        return await self.read_1(id)

    async def delete(self, id: ObjectID) -> bool:
        if not (_id := self.get_id(id)):
            return False
        if not (data := await self.db.delete_one({"_id": _id})):
            return False
        return data.deleted_count == 1

    @staticmethod
    def get_id(id: str) -> Optional[ObjectId]:
        try:
            _id = ObjectId(id)
            return _id
        except InvalidId as e:
            logger.warning("%s - %s", e.__class__.__name__, e)
            return None


class DataAccessLayerCached(DataAccessLayer, CacheAccessLayerBase):
    def __init__(self, name: str, cache_duration: int, max_limit: int = 1000) -> None:
        super().__init__(name, max_limit)
        self.cache = cache
        self.cache_duration: int = cache_duration

    async def read_all(self, query: Query = {}, limit: int = 1000) -> List[ModelType]:
        limit = min(limit, self.max_limit)
        key: str = f"{self.name} list: {query} limit:{limit}"

        if cache := self.cache.get(key):
            return json.loads(cache)

        if not (data := await super().read_all(query, limit)):
            return []

        self.cache.set(key, json.dumps(data), self.cache_duration)
        return data

    async def read_1(self, id: ObjectID) -> Optional[ModelType]:
        key: str = f"{self.name} id: {id}"

        if cache := self.cache.get(key):
            return json.loads(cache)

        if not (data := await super().read_1(id)):
            return None

        self.cache.set(key, json.dumps(data), self.cache_duration)
        return data
