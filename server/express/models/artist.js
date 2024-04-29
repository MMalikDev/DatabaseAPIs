import mongoose from "mongoose";

const ArtistSchema = new mongoose.Schema(
  {
    first_name: { type: String, required: true },
    last_name: { type: String, required: true },
    nationality: { type: String, required: true },

    songs: [{ type: mongoose.Schema.Types.ObjectId, ref: "Song" }],
    albums: [{ type: mongoose.Schema.Types.ObjectId, ref: "Album" }],

    date_created: { type: Date },
    last_modified: { type: Date },
  },
  { timestamps: { createdAt: "date_created", updatedAt: "last_modified" } }
);
export default mongoose.model("Artist", ArtistSchema);
