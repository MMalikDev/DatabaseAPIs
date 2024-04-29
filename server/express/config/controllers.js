import Song from "../models/song.js";
import Album from "../models/album.js";
import Artist from "../models/artist.js";
import Book from "../models/books.js";
import { applyConfiguration } from "../controllers/factory.js";

// Defaults
const defaultFilter = {
  date_created: false,
  last_modified: false,
  role: false,
  __v: false,
};

// Configuration
const configSong = {
  controllerConfig: {
    name: "Song",
    fieldId: "songId",
  },

  dalConfig: {
    model: Song,
    filter: defaultFilter,
    links: [
      {
        path: "album",
        model: "Album",
        foreignPath: "songs",
      },
      {
        path: "artist",
        model: "Artist",
        foreignPath: "songs",
      },
    ],
  },
};

const configAlbum = {
  controllerConfig: {
    name: "Album",
    fieldId: "albumId",
  },

  dalConfig: {
    model: Album,
    filter: defaultFilter,
    links: [
      {
        path: "songs",
        model: "Song",
        foreignPath: "album",
      },
      {
        path: "artist",
        model: "Artist",
        foreignPath: "albums",
      },
    ],
  },
};

const configArtist = {
  controllerConfig: {
    name: "Artist",
    fieldId: "artistId",
  },

  dalConfig: {
    model: Artist,
    filter: defaultFilter,
    links: [
      {
        path: "songs",
        model: "Song",
        foreignPath: "artist",
      },
      {
        path: "albums",
        model: "Album",
        foreignPath: "artist",
      },
    ],
  },
};
const configBook = {
  controllerConfig: {
    name: "Book",
    fieldId: "bookId",
  },

  dalConfig: {
    model: Book,
    filter: defaultFilter,
  },
};

// Initialize dataHandlers & controllers
const configs = [configSong, configAlbum, configArtist, configBook];
const { dataHandlers, controllers } = applyConfiguration(configs);

export { dataHandlers, controllers };
