export default function dnaPosition(dnaObjects, covered_LeftPosition, covered_RightPosition) {
  let dnaObjectsSort = []
  
  if(covered_LeftPosition && covered_RightPosition){
    dnaObjects.forEach(object => {
      if ((object.leftEndPosition >= covered_LeftPosition && object.rightEndPosition <= covered_RightPosition)||
        (object.leftEndPosition <= covered_RightPosition && object.rightEndPosition >= covered_LeftPosition)) {
        dnaObjectsSort.push(object)
      }
    })
  }else{
    dnaObjectsSort = dnaObjects
  }

  dnaObjectsSort.sort(function (a, b) {
    if (a?.leftEndPosition > b?.leftEndPosition) {
      return 1;
    }
    if (a?.leftEndPosition < b?.leftEndPosition) {
      return -1;
    }
    return 0;
  });
  return dnaObjectsSort;
}