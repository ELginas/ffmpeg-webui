export function stopPropagation(fn) {
  return function (event) {
    event.stopPropagation();
    fn.call(this, event);
  };
}

export function getKey(obj, key, value) {
  return obj.filter((el) => el[key] === value)[0];
}

export function escapeString(str) {
    const isAlphanumeric = /^[a-zA-Z0-9]+$/.test(str)
    if (isAlphanumeric) {
        return str;
    }
    const newStr = `'${str.replaceAll("'", "\\'")}'`
    return newStr;
}