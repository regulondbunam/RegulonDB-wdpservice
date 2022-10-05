// Terminator 0.10.0
/**
 * Falta testear
 * head de la figura se sale de posicion
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
//import { label } from "./label";
import { terminator_dp } from "./features_default_properties/index.js";

export default function DrawTerminator({
  id,
  canva,
  anchor,
  dna,
  separation = 20,
  leftEndPosition = 10,
  rightEndPosition = 50,
  labelName = "Name",
  strand = "forward",
  color = "aqua",
  opacity = 1,
  stroke = {},
  font = {},
  tooltip = "",
  height,
  onClick
}) {
  if (!canva || !dna || !id || leftEndPosition > rightEndPosition) {
    return null;
  }
  stroke = stroke_validate(stroke, terminator_dp.stroke);
  font = font_validate(font, terminator_dp.font);
  color = color_validate(color, "#000000");
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 1;
    strand = anchor.strand;
  }
  if(!height){
    height = terminator_dp.height
  }
  // attributes
  const x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  let terminator_width = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  let terminator_height = height //+ separation;
  //attributes
  
  let headSize = terminator_height * terminator_dp.proportions.head
  let bodyHeight = terminator_height * terminator_dp.proportions.body + 0.0875*headSize
  let bodyWidth = terminator_width * terminator_dp.proportions.foot
  let footHeight = terminator_height * terminator_dp.proportions.foot
  let footWidth = terminator_width/2 - bodyWidth/2
  
  // positions
  let posX = x + dna.x;
  let posY = dna.y - terminator_height;
  // draw BODY
  const headMiddle = headSize/2
  const headInset = 0.9125*headMiddle
  let body = undefined
  //console.log("aaa "+separation);
  if(strand === "reverse"){
    body = canva.path(
      "M "+posX+","+dna.y+
      "v "+footHeight+
      "h "+footWidth+
      "v "+bodyHeight+ 
      "q -"+(0.25*headSize)+" 0 -"+(0.25*headSize)+" "+(headInset)+
      "q 0 "+headMiddle+" "+headMiddle+" "+headMiddle+
      "q "+headMiddle+" 0 "+headMiddle+" -"+headMiddle+
      "q 0 -"+(headInset)+" -"+(0.25*headSize)+" -"+(headInset)+
      "v -"+bodyHeight+
      "h "+footWidth+
      "v -"+footHeight
    );
  } else {
    body = canva.path(
      "M "+posX+","+dna.y+
      "v -"+footHeight+
      "h "+footWidth+
      "v -"+bodyHeight+ 
      "q -"+(0.25*headSize)+" 0 -"+(0.25*headSize)+" -"+(headInset)+
      "q 0 -"+headMiddle+" "+headMiddle+" -"+headMiddle+
      "q "+headMiddle+" 0 "+headMiddle+" "+headMiddle+
      "q 0 "+(headInset)+" -"+(0.25*headSize)+" "+(headInset)+
      "v "+bodyHeight+
      "h "+footWidth+
      "v "+footHeight
    );
  }
  body.attr({
    "fill-opacity": 0
  });
  body.stroke(stroke);
  body.opacity(opacity);

  var group = canva.group();
  group.add(body);
  //text
  /*
  if(labelName){
    const text = label({
      canvas: canva,
      x: headX,
      y: headY - font.size,
      text: labelName,
      font: font
    });
    if(strand === "reverse"){
      text.transform({
        translateY: (bodyHeight + bodyFootH + 30) * 2
      });
    }
  }*/
  
  //Actions
  if (onClick) {
   group.attr({
      cursor: "pointer"
    })
   group.click(onClick);
  }
  //tooltip
  group.attr({
    "data-tip": "",
    "data-for": `"${canva.node?.id}-${id}"`
  });

  return {
    id: id,
    canva: canva,
    draw: group,
    posX: posX,
    posY: posY,
    terminator_width: terminator_width,
    height: terminator_height,
    dna: dna,
    separation: separation,
    leftEndPosition: leftEndPosition,
    rightEndPosition: rightEndPosition,
    labelName: labelName,
    strand: strand,
    color: color,
    opacity: color,
    stroke: stroke,
    font: font,
    objectType: "terminator",
    tooltip: tooltip
  };
}


/*
  //Head attributes
  let headH = proportion;
  let terminatorH = bodyHeight + headH;
  let headScale = () => {
    return (proportion * 33) / 25 / 33;
  };
  let headWidth = () => {
    return 35 - ((25 - proportion) * 8) / 10;
  };
  let headHeight = () => {
    return 35 - ((25 - proportion) * 8) / 10;
  };
  */