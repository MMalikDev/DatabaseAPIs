from faker import Faker


class Songs:
    def __init__(self, *args, **kwargs) -> None:

        fake = Faker()

        self.title = fake.catch_phrase()

        self.album = []
        self.artist = []
