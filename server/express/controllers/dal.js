import { getLinks, getReferences } from "./utils.js";

const defaultOptions = {
  model: null,
  filter: {},
  links: [],
  reference: [],
  defaultForeignPath: null,
};

const defaultSettings = {
  get: { populate: true },
  getCollection: { populate: false },
};

export default class DataAccessLayer {
  constructor(options) {
    this.model = options.model || defaultOptions.model;
    this.filter = options.filter || defaultOptions.filter;
    this.defaultForeignPath =
      options.defaultForeignPath || defaultOptions.defaultForeignPath;

    this.links =
      options.links ||
      getLinks(this.model, this.defaultForeignPath) ||
      defaultOptions.links;

    this.reference =
      options.reference ||
      getReferences(this.links, this.filter) ||
      defaultOptions.reference;
  }

  // Get a collection of documents
  getCollection(query, options = {}) {
    const populate = options.populate || defaultSettings.getCollection.populate;
    const data = this.model.find(query).lean();

    return populate
      ? data.lean().populate(this.reference).select(this.filter)
      : data.select(this.filter);
  }

  // Create an document
  create(data) {
    return this.model.create(data);
  }

  // Get an document
  get(query, options = {}) {
    const populate = options.populate || defaultSettings.get.populate;
    const data = this.model.findOne(query).lean();

    return populate
      ? data.populate(this.reference).select(this.filter)
      : data.select(this.filter);
  }

  // Update an document
  update(id, data) {
    return this.model.findByIdAndUpdate(id, data);
  }

  // Remove an document
  remove(id) {
    return this.model.findByIdAndRemove(id);
  }
}
