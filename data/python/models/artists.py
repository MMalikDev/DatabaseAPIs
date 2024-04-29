from faker import Faker


class Artists:
    def __init__(self, *args, **kwargs) -> None:

        fake = Faker()

        self.first_name = fake.first_name()
        self.last_name = fake.last_name()

        self.nationality = fake.country()

        self.songs = []
        self.albums = []
