import DataAccessLayer from "./dal.js";
import Controller from "./base.js";

function applyConfiguration(configs) {
  if (!configs) throw new Error("No configurations were provided.");
  if (!Array.isArray(configs)) throw new Error("Invalid configurations");

  let dataHandlers = {};
  for (const config of configs) {
    const { dalConfig, controllerConfig } = config;
    const newDal = new DataAccessLayer(dalConfig);
    dataHandlers[controllerConfig.name] = newDal;
  }

  let controllers = {};
  for (const config of configs) {
    const { controllerConfig } = config;
    const newController = new Controller(controllerConfig, dataHandlers);
    controllers[controllerConfig.name] = newController;
  }

  return { dataHandlers, controllers };
}

export { applyConfiguration };
