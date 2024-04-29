from lib.test import TestCustom
from router.endpoints.songs import SongController

song_tests = TestCustom(
    "songs",
    router=SongController.router,
    nonexisting_id=0,
    example={
        "title": "Sample Title",
        "album_id": None,
    },
)
