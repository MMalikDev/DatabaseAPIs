import mongoose from "mongoose";

const AlbumSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },

    songs: [{ type: mongoose.Schema.Types.ObjectId, ref: "Song" }],
    artist: [{ type: mongoose.Schema.Types.ObjectId, ref: "Artist" }],

    date_created: { type: Date },
    last_modified: { type: Date },
  },
  { timestamps: { createdAt: "date_created", updatedAt: "last_modified" } }
);

export default mongoose.model("Album", AlbumSchema);
