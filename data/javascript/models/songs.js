import { faker } from "@faker-js/faker";

class Songs {
  constructor() {
    this.title = faker.music.songName();

    this.artist = [];
    this.album = [];

    this.date_created = faker.date.anytime();
    this.last_modified = faker.date.anytime();
  }
}

export { Songs };
