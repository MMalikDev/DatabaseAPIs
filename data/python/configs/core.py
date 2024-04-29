from lib.utilities import load_variable


class Settings:
    SQL_URI: str = load_variable("SQL_URI", "sqlite+pysqlite:///sqlite.db")

    NO_SQL_URI: str = load_variable("NO_SQL_URI", "mongodb://admin:pass@mongo")
    DATABASE: str = load_variable("DATABASE", "admin")

    SIZE: int = int(load_variable("SIZE", 10))


settings = Settings()
