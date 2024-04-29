const settings = {
  DATABASE_URI: process.env.DATABASE_URI || "mongodb://admin:pass@mongo",
  DATABASE: process.env.DATABASE || "admin",
  SIZE: parseInt(process.env.SIZE) || 10,
};

export { settings };
