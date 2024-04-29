async function linkReferences(data, links) {
  if (!links.length) return;
  const newID = data._id;
  for (const link of links) {
    const { path, model, foreignPath, modelDal } = link;
    const idToLink = data[path];
    if (!idToLink.length) continue;

    try {
      const document = await modelDal.get(
        { _id: idToLink },
        { populate: false }
      );

      if (document) {
        document[foreignPath].push(newID);
        const documentUpdate = {
          [foreignPath]: document[foreignPath],
        };

        await modelDal.update({ _id: document._id }, documentUpdate);
      }
    } catch (error) {
      console.error(
        `Error linking reference for ${newID} ` +
          `in the ${foreignPath} field of the ${model} model: ` +
          error.message
      );
    }
  }

  return;
}

export { linkReferences };
