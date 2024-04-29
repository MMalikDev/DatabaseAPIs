from lib.test import TestPytest
from router.endpoints.songs import SongController


class TestPytest(TestPytest):
    def __init__(self, methodName="runTest") -> None:

        super().__init__(
            methodName,
            name="songs",
            router=SongController.router,
            nonexisting_id=0,
            example={
                "title": "Sample Title",
                "album_id": None,
            },
        )
