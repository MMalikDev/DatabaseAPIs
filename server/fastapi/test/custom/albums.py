from lib.test import TestCustom
from router.endpoints.albums import AlbumController

album_tests = TestCustom(
    "albums",
    nonexisting_id=0,
    router=AlbumController.router,
    example={
        "title": "Sample Title",
        "artist_id": None,
        "song_id": None,
    },
)
