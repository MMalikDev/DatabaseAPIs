from faker import Faker


class Albums:
    def __init__(self, *args, **kwargs) -> None:

        fake = Faker()

        self.title = fake.catch_phrase()
        self.songs = []
        self.artist = []
