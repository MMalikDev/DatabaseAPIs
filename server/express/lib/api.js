function pagination(req, data, defaultLimit = process.env.LIMIT || 20) {
  const limit = req.query.limit || defaultLimit;
  const page = req.query.page || 1;

  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;

  return data.slice(startIndex, endIndex) || [];
}

export { pagination };
