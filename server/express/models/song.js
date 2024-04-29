import mongoose from "mongoose";

const SongSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    genre: { type: String },

    album: [{ type: mongoose.Schema.Types.ObjectId, ref: "Album" }],
    artist: [{ type: mongoose.Schema.Types.ObjectId, ref: "Artist" }],

    date_created: { type: Date },
    last_modified: { type: Date },

    role: { type: String, default: "readWrite" },
  },
  { timestamps: { createdAt: "date_created", updatedAt: "last_modified" } }
);

export default mongoose.model("Song", SongSchema);
