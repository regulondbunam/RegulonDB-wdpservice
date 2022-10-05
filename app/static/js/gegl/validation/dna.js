import { toInt } from "./util.js";

export function validateDNA(dnaObjects, covered_LeftPosition, covered_RightPosition) {
  if (!dnaObjects) {
    return undefined;
  }
  const dna = dnaObjects.find((feature) => feature?.objectType === "dna");
  if (dna) {
    return dna;
  }
  let dna_left = undefined;
  let dna_right = undefined;
  if (covered_LeftPosition && covered_RightPosition) {
    if (covered_LeftPosition > covered_RightPosition) {
        console.log("validateDNA: covered_LeftPosition > covered_RightPosition");
        return undefined
    }
    dna_left = covered_LeftPosition;
    dna_right = covered_RightPosition;
  } else {
    dnaObjects.map((feature, idx) => {
      if (feature?.leftEndPosition && feature?.rightEndPosition) {
        let leftEndPosition = toInt(feature?.leftEndPosition);
        let rightEndPosition = toInt(feature?.rightEndPosition);
        let plusLeft = ("" + feature?.leftEndPosition).indexOf("+");
        let plusRight = ("" + feature?.leftEndPosition).indexOf("+");
        if (plusLeft === -1 && !dna_left) {
          dna_left = leftEndPosition;
        }
        if (plusRight === -1 && !dna_right) {
          dna_right = rightEndPosition;
        }
        if (dna_left > leftEndPosition && plusLeft === -1) {
          dna_left = leftEndPosition;
        }
        if (dna_right < rightEndPosition && plusRight === -1) {
          dna_right = rightEndPosition;
        }
      }
      return null;
    });
  }
  //console.log(dnaFeatures_data);
  return {
    _id: "DNA-Default",
    labelFont: "",
    labelRGGColor: "",
    labelName: "",
    labelSize: "12",
    leftEndPosition: dna_left.toString(),
    lineRGBColor: "0,0,0",
    lineType: "",
    lineWidth: "",
    objectType: "dna",
    objectRGBColor: "",
    rightEndPosition: dna_right.toString(),
    strand: "forward",
    tooltip: ""
  };
}
