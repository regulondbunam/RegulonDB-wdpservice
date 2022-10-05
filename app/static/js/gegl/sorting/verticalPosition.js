import { getPropertiesByObjectType } from "../features_default_properties/index.js";
import { WhoGoesUp } from "./verticalRules.js";

export default function verticalPosition(geneticElements, dna) {
    //console.log(geneticElements);
    //assign level
    geneticElements.forEach(dnaObject => {
        dnaObject.level = 1;
    });
    // assign levels to geneticElements
    let height = undefined;
    let width = undefined;
    let levelForward = 1;
    let levelReverse = 1;
    let controlFlag = 0
    do {
        for (let i = 0; i < geneticElements.length; i++) {
            for (let j = 0; j < geneticElements.length; j++) {
                if (geneticElements[i]._id !== geneticElements[j]._id && i < j) {
                    if (isCollision(geneticElements[i], geneticElements[j])) {
                        geneticElements[j].level++
                        if (geneticElements[j].strand === 'forward') {
                            if (levelForward < geneticElements[j].level) {
                                levelForward = geneticElements[j].level;
                            }
                        } else {
                            if (levelReverse < geneticElements[j].level) {
                                levelReverse = geneticElements[j].level;
                            }
                        }
                    }
                }
            }
        }
        controlFlag++
    } while (isCollisions(geneticElements) && controlFlag < 10);
    controlFlag = 0

    //console.log("levelForward", levelForward);
    //console.log("levelReverse", levelReverse);

    //assign positions to geneticElements
    let maxHeightObject = undefined;
    if (dna) {
        if (levelForward >= levelReverse) {
            maxHeightObject = dna.forwardActive / levelForward;
        } else {
            maxHeightObject = dna.reverseActive / levelReverse;
        }
    }
    //console.log("maxHeightObject", maxHeightObject);
    geneticElements.forEach(dnaObject => {
        let properties = getPropertiesByObjectType(dnaObject.objectType);
        dnaObject.separation = 0
        dnaObject.width = dnaObject.rightEndPosition - dnaObject.leftEndPosition
        if (dnaObject.width === 0) {
            dnaObject.width = properties.width
        }
        dnaObject.x = dnaObject.leftEndPosition
        if (dna) {
            if (properties.height > maxHeightObject) {
                dnaObject.height = maxHeightObject
            } else {
                dnaObject.height = properties.height;
            }
            // console.log(dnaObject.height);
            dnaObject.y = dna.y - dnaObject.height
            dnaObject.previousY = dna.y - dnaObject.height
        }
    })

    //assign separation
    do {
        for (let i = 0; i < geneticElements.length; i++) {
            for (let j = 0; j < geneticElements.length; j++) {
                if (geneticElements[i]._id !== geneticElements[j]._id && i < j) {
                    if (isOverlap(geneticElements[i], geneticElements[j])) {
                        //console.log("overlap", geneticElements[i]._id, geneticElements[j]._id);
                        let elementToMove = j
                        let elementStay = i
                        if (WhoGoesUp(geneticElements[i], geneticElements[j]) === geneticElements[i]._id) {
                            elementToMove = i
                            elementStay = j
                        }
                        if (geneticElements[elementToMove].strand === 'forward') {
                            geneticElements[elementToMove].y = geneticElements[elementToMove].y - geneticElements[elementStay].height;
                        } else {
                            geneticElements[elementToMove].y = geneticElements[elementToMove].y + geneticElements[elementStay].height
                        }
                    }
                }
            }
        }
    } while (isOverlaps(geneticElements) && controlFlag < 5);
    controlFlag = 0
    geneticElements.forEach(dnaObject => {
        dnaObject.separation = Math.abs(dnaObject.y - dnaObject.previousY)
    });

    console.log(geneticElements);

    return { geneticElements: geneticElements, height: height, width: width };
}

function isCollision(dnaObjectA, dnaObjectB) {
    if (dnaObjectA.strand !== dnaObjectB.strand || dnaObjectA._id === dnaObjectB._id || dnaObjectA.level !== dnaObjectB.level) {
        return false;
    }
    return (dnaObjectA.x < dnaObjectB.x + dnaObjectB.width &&
        dnaObjectB.x < dnaObjectA.x + dnaObjectA.width);
    /*
    return ((dnaObjectA.rightEndPosition >= dnaObjectB.leftEndPosition &&
        dnaObjectB.rightEndPosition >= dnaObjectA.rightEndPosition) &&
        (dnaObjectA.level === dnaObjectB.level))
        */
}

function isOverlap(dnaObjectA, dnaObjectB) {
    if (dnaObjectA.strand !== dnaObjectB.strand || dnaObjectA._id === dnaObjectB._id) {
        return false;
    }
    /*
    if(dnaObjectA._id === "" && dnaObjectB._id === ""){
        console.log("1", dnaObjectA.x + " < "+ dnaObjectB.x + dnaObjectB.width );
        console.log("2", dnaObjectB.x < dnaObjectA.x + dnaObjectA.width );
        console.log("3", dnaObjectA.y < dnaObjectB.y + dnaObjectB.height);
        console.log("4", dnaObjectB.y < dnaObjectA.y + dnaObjectA.height);
    }
    */
    return (dnaObjectA.x < dnaObjectB.x + dnaObjectB.width &&
        dnaObjectB.x < dnaObjectA.x + dnaObjectA.width &&
        dnaObjectA.y < dnaObjectB.y + dnaObjectB.height &&
        dnaObjectB.y < dnaObjectA.y + dnaObjectA.height);
}

function isOverlaps(geneticElements) {
    for (let i = 0; i < geneticElements.length; i++) {
        for (let j = 0; j < geneticElements.length; j++) {
            if (geneticElements[i]._id !== geneticElements[j]._id && i < j) {
                if (isOverlap(geneticElements[i], geneticElements[j])) {
                    return true
                }
            }
        }
    }
    return false
}

function isCollisions(geneticElements) {
    for (let i = 0; i < geneticElements.length; i++) {
        for (let j = 0; j < geneticElements.length; j++) {
            if (geneticElements[i]._id !== geneticElements[j]._id && i < j) {
                if (isCollision(geneticElements[i], geneticElements[j])) {
                    return true
                }
            }
        }
    }
    return false
}
/**
 * a.x < b.x + b.w &&
    b.x < a.x + a.w &&
    a.y < b.y + b.h &&
    b.y < a.y + a.h);
 */