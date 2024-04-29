import { MongoClient, ServerApiVersion } from "mongodb";
import { settings } from "../configs/core.js";

const options = {
  serverApi: {
    version: ServerApiVersion.v1,
    deprecationErrors: true,
    strict: true,
  },
};

const client = new MongoClient(settings.DATABASE_URI, options);
const database = client.db(settings.DATABASE);

export { database };
