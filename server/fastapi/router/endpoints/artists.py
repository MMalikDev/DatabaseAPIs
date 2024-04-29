from controllers.crud.sql.synchronous import Controller
from models.artists import Artist, ArtistSchema, ArtistSchemaCreate, ArtistSchemaUpdate

ArtistController = Controller(
    "artists",
    cache=True,
    Model=Artist,
    SchemaBase=ArtistSchema,
    SchemaCreate=ArtistSchemaCreate,
    SchemaUpdate=ArtistSchemaUpdate,
)

ArtistController.add_default_endpoints()
