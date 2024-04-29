from lib.test import TestPytest
from router.endpoints.items import ItemController


class TestPytest(TestPytest):
    def __init__(self, methodName="runTest") -> None:

        super().__init__(
            methodName,
            name="items",
            router=ItemController.router,
            nonexisting_id=0,
            example={
                "title": "Sample Title",
                "description": "Sample Description",
            },
        )
