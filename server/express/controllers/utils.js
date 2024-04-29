function getLinks(model, foreignPath) {
  const defaultLink = [];
  if (!foreignPath) return defaultLink;

  const schema = model.schema.obj;
  const links = [];
  for (const [key, value] of Object.entries(schema)) {
    if (!Array.isArray(value) || !value.length || !value[0].ref) continue;
    links.push({
      path: key,
      model: dataHandlers[value[0].ref],
      foreignPath: foreignPath,
    });
  }
  return links;
}

function getReferences(links, filter) {
  const defaultReference = [];
  if (links.length == 0) return defaultReference;

  let references = [];
  for (const link of links) {
    references.push({
      path: link.path,
      model: link.model,
      select: filter,
    });
  }
  return references;
}

function getModelDal(model, dataHandlers) {
  const links = model.links.map((link) => ({
    ...link,
    modelDal: dataHandlers[link.model],
  }));
  return links;
}

export { getLinks, getReferences, getModelDal };
