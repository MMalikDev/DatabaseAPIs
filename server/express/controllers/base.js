import { getModelDal } from "./utils.js";
import { linkReferences } from "./relation.js";
import { handleError, handleSuccess } from "./handler.js";
import { pagination } from "../lib/api.js";
import { getCallerName } from "../lib/utils.js";
import mongoose from "mongoose";

const defaultOptions = {
  name: "",
  fieldId: "id",
  model: new mongoose.Schema(),
  links: [],
};

async function runQuery(res, method, name, callback) {
  try {
    const data = await callback();
    handleSuccess(res, method, name, data);
  } catch (error) {
    handleError(res, method, name, error);
  }
}

export default class Controller {
  constructor(options, dataHandlers) {
    this.name = options.name || defaultOptions.name;
    this.fieldId = options.fieldId || defaultOptions.fieldId;
    this.model = dataHandlers[this.name] || defaultOptions.model;
    this.links = getModelDal(this.model, dataHandlers) || defaultOptions.links;

    this.list = async (req, res, next) => {
      const method = getCallerName();

      runQuery(res, method, this.name, async () => {
        const collection = await this.model.getCollection({});
        return pagination(req, collection);
      });
    };

    this.create = async (req, res, next) => {
      const method = getCallerName();
      const body = req.body;

      runQuery(res, method, this.name, async () => {
        const data = await this.model.create(body);
        linkReferences(data, this.links);
        return data;
      });
    };

    this.read = async (req, res, next) => {
      const method = getCallerName();
      const itemId = req.params[this.fieldId];

      runQuery(res, method, this.name, async () => {
        return await this.model.get({ _id: itemId });
      });
    };

    this.update = async (req, res, next) => {
      const method = getCallerName();
      const itemId = req.params[this.fieldId];
      const body = req.body;

      runQuery(res, method, this.name, async () => {
        const data = await this.model.update({ _id: itemId }, body);
        linkReferences(data, this.links);
        return data;
      });
    };

    this.delete = async (req, res, next) => {
      const method = getCallerName();
      const itemId = req.params[this.fieldId];

      runQuery(res, method, this.name, async () => {
        return await this.model.remove({ _id: itemId });
      });
    };
  }
}
