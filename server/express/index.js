import mongoose from "mongoose";
import express from "express";
import cors from "cors";
import expressLayouts from "express-ejs-layouts";
import router from "./routes/index.js";
import setCache from "./lib/cache.js";
import config from "./config/core.js";
import { errorLogger, logger } from "./lib/logger.js";

// Connect to MongoDB
mongoose
  .connect(config.MongoURL)
  .then(() => console.info("Connected to MongoDB"))
  .catch((error) => console.error("Error connecting to MongoDB:", error));

const app = express();

// Set Template Engine
app.use(expressLayouts);
app.set("layout", "./layout");
app.set("view engine", "ejs");

// Middleware
app.use(cors());
app.use(setCache);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Routes
app.use(logger);
router(app);
app.use(errorLogger);

// Start Server
app.listen(config.PORT, () => console.info("http://express.localhost"));
