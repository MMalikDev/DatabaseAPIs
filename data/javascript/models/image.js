import { faker } from "@faker-js/faker";

class Images {
  constructor() {
    this.author = faker.person.fullName();
    this.download_url = faker.image.urlLoremFlickr();
    this.description = faker.lorem.paragraphs({ min: 5, max: 10 });
  }
}

export { Images };
