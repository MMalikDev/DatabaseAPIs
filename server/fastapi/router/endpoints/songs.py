from controllers.crud.sql.synchronous import Controller
from models.songs import Song, SongSchema, SongSchemaCreate, SongSchemaUpdate

SongController = Controller(
    "songs",
    cache=True,
    Model=Song,
    SchemaBase=SongSchema,
    SchemaCreate=SongSchemaCreate,
    SchemaUpdate=SongSchemaUpdate,
)

SongController.add_default_endpoints()
