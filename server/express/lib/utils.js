// Experimental Functions
function getCallerName() {
  return new Error("_").stack
    .split("\n")[2]
    .replace(/^\s+at\s+(.+?)\s.+/g, "$1");
  // REGEX: ' at <Name> ' => '<Name>'
}

function varToString(varObj) {
  return Object.keys(varObj)[0];
}

export { getCallerName };
