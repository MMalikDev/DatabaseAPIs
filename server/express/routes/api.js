import express from "express";
import songRouter from "./endpoints/song.js";
import albumRouter from "./endpoints/album.js";
import artistRouter from "./endpoints/artist.js";
import bookRouter from "./endpoints/book.js";

const router = express.Router();
router.use("/books", bookRouter);
router.use("/songs", songRouter);
router.use("/albums", albumRouter);
router.use("/artists", artistRouter);

export default router;
