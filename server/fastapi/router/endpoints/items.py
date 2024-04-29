from controllers.crud.sql.synchronous import Controller
from models.items import Item, ItemSchema, ItemSchemaCreate, ItemSchemaUpdate

ItemController = Controller(
    "items",
    cache=False,
    Model=Item,
    SchemaBase=ItemSchema,
    SchemaCreate=ItemSchemaCreate,
    SchemaUpdate=ItemSchemaUpdate,
)


ItemController.add_default_endpoints()
