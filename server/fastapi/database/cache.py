from configs.core import settings
from redis import Redis

cache = Redis.from_url(settings.CACHE_URI)
