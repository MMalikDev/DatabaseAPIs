from lib.test import TestCustom
from router.endpoints.artists import ArtistController

artist_tests = TestCustom(
    "artists",
    router=ArtistController.router,
    nonexisting_id=0,
    example={
        "first_name": "John",
        "last_name": "Doe",
        "nationality": "Atlantis",
        "album_id": None,
    },
)
