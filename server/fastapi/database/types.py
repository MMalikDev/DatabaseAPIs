from typing import Any, Dict, Union

from database import Base
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.database import Database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

ID = int
ObjectID = str

ModelType = Base
CreateType = Dict[str, Any]
UpdateType = Dict[str, Any]
SchemaType = Dict[str, Any]

Query = Dict[str, str]
SessionType = Union[Session, AsyncSession, Database, AsyncIOMotorDatabase]
