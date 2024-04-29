from controllers.crud.sql.synchronous import Controller
from models.albums import Album, AlbumSchema, AlbumSchemaCreate, AlbumSchemaUpdate

AlbumController = Controller(
    "albums",
    cache=True,
    Model=Album,
    SchemaBase=AlbumSchema,
    SchemaCreate=AlbumSchemaCreate,
    SchemaUpdate=AlbumSchemaUpdate,
)

AlbumController.add_default_endpoints()
