import { faker } from "@faker-js/faker";

class Albums {
  constructor() {
    this.title = faker.music.songName();

    this.artist = [];
    this.songs = [];

    this.date_created = faker.date.anytime();
    this.last_modified = faker.date.anytime();
  }
}

export { Albums };
