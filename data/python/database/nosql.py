from configs.core import settings
from pymongo import MongoClient

client = MongoClient(settings.NO_SQL_URI)
database = client[settings.DATABASE]
