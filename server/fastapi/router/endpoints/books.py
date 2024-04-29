from controllers.crud.nosql.synchronous import Controller
from models.books import Book, BookCreate, BookUpdate

BookController = Controller(
    name="book",
    cache=True,
    ModelBase=Book,
    SchemaUpdate=BookUpdate,
    SchemaCreate=BookCreate,
)

BookController.add_default_endpoints()
