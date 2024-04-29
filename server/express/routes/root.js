import express from "express";
import { dataHandlers } from "../config/controllers.js";

const router = express.Router();

const options = { populate: true };

router
  .route("/")
  //
  .get(async (req, res) => {
    const context = {
      data: {
        books: await dataHandlers.Book.getCollection({}, options),
        songs: await dataHandlers.Song.getCollection({}, options),
        albums: await dataHandlers.Album.getCollection({}, options),
        artists: await dataHandlers.Artist.getCollection({}, options),
      },
    };

    res.render("index", context);
  });

export default router;
