from lib.test import TestPytest
from router.endpoints.books import BookController


class TestPytest(TestPytest):
    def __init__(self, methodName="runTest") -> None:
        super().__init__(
            methodName,
            name="items",
            router=BookController.router,
            id_field="_id",
            example={
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "...",
            },
        )
