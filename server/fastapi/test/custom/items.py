from lib.test import TestCustom
from router.endpoints.items import ItemController

item_tests = TestCustom(
    "items",
    router=ItemController.router,
    nonexisting_id=0,
    example={
        "title": "Sample Title",
        "description": "Sample Description",
    },
)
