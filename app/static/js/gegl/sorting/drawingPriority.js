import {getPropertiesByObjectType } from "../features_default_properties/index.js";

  export default function drawingPriority(dnaObjects) {
    // priority assignation
    dnaObjects.forEach(dnaObject => {
        dnaObject.drawPriority = getPropertiesByObjectType(dnaObject.objectType).drawPriority;
    });
    // sort by priority
    dnaObjects.sort(function (a, b) {
      if (a?.drawPriority > b?.drawPriority) {
        return 1;
      }
      if (a?.drawPriority < b?.drawPriority) {
        return -1;
      }
      return 0;
    });
    return dnaObjects;
  }
  
  /**/
  