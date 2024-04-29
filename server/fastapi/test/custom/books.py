from lib.test import TestCustom
from router.endpoints.books import BookController

book_tests = TestCustom(
    "items",
    router=BookController.router,
    id_field="_id",
    example={
        "title": "Don Quixote",
        "author": "Miguel de Cervantes",
        "synopsis": "...",
    },
)
