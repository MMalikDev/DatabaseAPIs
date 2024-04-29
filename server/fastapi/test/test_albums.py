from lib.test import TestPytest
from router.endpoints.albums import AlbumController


class TestPytest(TestPytest):
    def __init__(self, methodName="runTest") -> None:
        super().__init__(
            methodName,
            name="albums",
            nonexisting_id=0,
            router=AlbumController.router,
            example={
                "title": "Sample Title",
                "artist_id": None,
                "song_id": None,
            },
        )
