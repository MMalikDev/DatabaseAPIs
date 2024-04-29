import { faker } from "@faker-js/faker";

class Artists {
  constructor() {
    this.first_name = faker.person.firstName();
    this.last_name = faker.person.lastName();
    this.nationality = faker.location.country();

    this.songs = [];
    this.albums = [];

    this.date_created = faker.date.anytime();
    this.last_modified = faker.date.anytime();
  }
}

export { Artists };
