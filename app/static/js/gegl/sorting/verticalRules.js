import { getPropertiesByObjectType } from "../features_default_properties/index.js";

export function WhoGoesUp(dnaObject_A, dnaObject_B) {
    let properties_A = getPropertiesByObjectType(dnaObject_A.objectType);
    let properties_B = getPropertiesByObjectType(dnaObject_B.objectType);
    if (properties_A.verticalPriority > properties_B.verticalPriority) {
        return dnaObject_A._id;
    }
    return dnaObject_B._id;
}