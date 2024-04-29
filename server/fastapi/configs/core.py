from datetime import timedelta
from secrets import token_urlsafe
from urllib.parse import urlparse

from lib.utilities import load_bool, load_variable, logger


def get_random_secret() -> str:
    secret = token_urlsafe(32)
    logger.info("One time random secret key: %s", secret)
    return secret


def get_parsed_url(name: str, default: str) -> str:
    url = load_variable(name, default)
    parsed_url = urlparse(url)
    return parsed_url.hostname


class Settings:
    # App
    STATIC_URL: str = get_parsed_url("STATIC_URL", "http://static.localhost")
    WEB_HOST: str = load_variable("WEB_HOST", "0.0.0.0")
    WEB_PORT: int = int(load_variable("WEB_PORT", "8080"))

    OPEN_USERS: bool = load_bool("OPEN_USERS")  # Test Extra User Routes (C.R.U.D.)

    # Database
    SQL_URI: str = load_variable("DATABASE_URI", "sqlite+pysqlite:///sqlite.db")
    NOSQL_URI: str = load_variable("DB_URI", "mongodb://admin:pass@mongo")
    CACHE_URI: str = load_variable("CACHE_URI", "redis://redis:6379/0")

    # Security
    ALGORITHM: str = load_variable("ALGORITHM", "HS256")
    SECRET_KEY: str = load_variable("SECRET_KEY", get_random_secret())

    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(
        minutes=float(load_variable("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 5))
    )  # 60 minutes * 24 hours * 5 days = 5 days
    RESET_TOKEN_EXPIRE_HOURS: timedelta = timedelta(
        hours=float(load_variable("RESET_TOKEN_EXPIRE_HOURS", 1))
    )  # 1 hours


settings = Settings()
