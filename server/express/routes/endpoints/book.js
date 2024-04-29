import express from "express";
import { controllers } from "../../config/controllers.js";

const router = express.Router();

const controller = controllers.Book;
const id = controller.fieldId;

router
  .route("/")
  //
  .get(controller.list)
  .post(controller.create);

router
  .route("/:" + id)
  .get(controller.read)
  .put(controller.update)
  .delete(controller.delete);

export default router;
