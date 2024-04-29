function getDetails(modelName) {
  const name = modelName.toUpperCase();

  return {
    "Controller.list": {
      success: `No ${name} Were Found`,
      error: `GET_${name}_ERROR`,
      status: 200,
    },
    "Controller.create": {
      success: ``,
      error: `CREATE_${name}_ERROR`,
      status: 201,
    },
    "Controller.read": {
      success: `Could Not Read ${name}`,
      error: `READ_${name}_ERROR`,
      status: 200,
    },
    "Controller.update": {
      success: `Could Not Update ${name}`,
      error: `UPDATE_${name}_ERROR`,
      status: 200,
    },
    "Controller.delete": {
      success: `Could Not Delete ${name}`,
      error: `REMOVE_${name}_ERROR`,
      status: 204,
    },
  };
}

function handleSuccess(res, method, name, data) {
  const details = getDetails(name)[method];
  let response = details.success ? data || { message: details.success } : data;
  return data
    ? res.status(details.status).json(response)
    : res.status(404).json(response);
}

function handleError(res, method, name, error) {
  console.error(error.message);
  const details = getDetails(name)[method];
  return res.status(500).json({ error: details.error });
}

export { handleSuccess, handleError };
