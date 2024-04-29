from typing import Any, Dict, List

from configs.core import settings
from database import DataAccessLayer, nosql
from lib.utilities import debug, logger
from models import SQL_Model, models_nosql, models_sql, noSQL_Model


def get_name(model) -> str:
    return str(model().__class__.__name__).lower()


def get_dataset(size: int, model: Any) -> List[Dict[str, Any]]:
    return [model().__dict__ for _ in range(size)]


# ---------------------------------------------------------------------- #
# Main Functions                                                         #
# ---------------------------------------------------------------------- #
def generator_noSQL(size: int, models: List[noSQL_Model]) -> None:
    for model in models:
        name = get_name(model.data)
        collection = nosql.database[name]
        dataset = get_dataset(size, model.data)

        count = collection.count_documents({})
        response = collection.insert_many(dataset)

        for id in response.inserted_ids:
            logger.debug("Added %s into noSQL - ID: %s", name, id)
        logger.info("Count of %s in noSQL DB: %i -> %i", name, count, count + size)


def generator_SQL(size: int, models: List[SQL_Model]) -> None:
    for model in models:
        name = get_name(model.data)
        dal = DataAccessLayer(model=model.db)
        dataset = get_dataset(size, model.data)

        for data in dataset:
            dal.create(data)

            logger.debug("Added %s into SQL %s", name, str(data))
        logger.info("Created %i new %s in SQL DB", size, name)


@debug
def main():
    generator_noSQL(settings.SIZE, models_nosql)
    generator_SQL(settings.SIZE, models_sql)


if __name__ == "__main__":
    main()
