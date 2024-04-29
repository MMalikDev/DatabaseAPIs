import rootRouter from "./root.js";
import apiRouter from "./api.js";

export default (app) => {
  app.use("/", rootRouter);
  app.use("/api", apiRouter);
};
