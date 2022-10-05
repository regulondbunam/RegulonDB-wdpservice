export function eMes(prop, inx) {
    console.warn(
        `The element in the index: ${inx} is not valid, problem with its property ${prop}`
    );
}

export function toInt(str = "") {
    if (Number.isInteger(str)) {
        return str;
    }
    str.toString().replace("+", "");
    return parseInt(str, 10);
}