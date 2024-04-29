from lib.test import TestPytest
from router.endpoints.artists import ArtistController


class TestPytest(TestPytest):
    def __init__(self, methodName="runTest") -> None:

        super().__init__(
            methodName,
            name="artists",
            router=ArtistController.router,
            nonexisting_id=0,
            example={
                "first_name": "John",
                "last_name": "Doe",
                "nationality": "Atlantis",
                "album_id": None,
            },
        )
