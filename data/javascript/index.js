import { modelsNoSQL } from "./models/index.js";
import { database } from "./database/nosql.js";
import { settings } from "./configs/core.js";

function getName(model) {
  return new model().constructor.name.toLowerCase();
}

function getDataset(size, model, ...props) {
  let dataset = [];
  for (let i = 0; i < size; i++) {
    const data = new model(props);
    dataset.push(data);
  }
  return dataset;
}

async function generator_noSQL(size, models) {
  for (const model of models) {
    const name = getName(model);
    const collection = database.collection(name);
    const dataset = getDataset(size, model);

    const count = await collection.countDocuments({});
    const response = await collection.insertMany(dataset);

    console.log(
      `Count of ${name} in noSQL DB: ${count} -> ${
        count + response.insertedCount
      }`
    );
  }
}

async function main() {
  await generator_noSQL(settings.SIZE, modelsNoSQL);
}

main();
