import mongoose from "mongoose";

const BookSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    synopsis: { type: String, required: true },

    date_created: { type: Date },
    last_modified: { type: Date },
  },
  { timestamps: { createdAt: "date_created", updatedAt: "last_modified" } }
);

export default mongoose.model("Book", BookSchema);
