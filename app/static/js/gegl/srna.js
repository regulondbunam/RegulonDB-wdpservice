//Draw RNA v 0.9.0
/**
 *
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import { label } from "./label.js";
import { srna_dp } from "./features_default_properties/index.js";

export default function DrawRna({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 10,
  labelName = "Name",
  strand = "forward",
  color,
  opacity = 0,
  stroke = {},
  font = {},
  tooltip = "",
  onClick
}) {
  if (!canva || !dna || !id | (leftEndPosition > rightEndPosition)) {
    return null;
  }
  stroke = stroke_validate(stroke, srna_dp.stroke);
  font = font_validate(font, srna_dp.font);
  color = color_validate(color, srna_dp.fill);

  // anchor effect
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  //attributes
  const srna_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  let srna_width = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  let srna = canva.group();
  let height = srna_dp.height


  //body attributes
  let bodyHeight = srna_dp.height / 3;
  let posX = srna_x + dna.x;
  let posY = dna.y - separation - srna_dp.height   ;

  //fet attributes
  let lineHeight = (srna_dp.height / 2);
  let lineSeparation = srna_dp.lineSeparation

  //Draw rect
  let body = canva.rect(srna_width, bodyHeight);
  body.move(posX, posY);
  body.stroke(stroke);
  body.fill(color);

  srna.add(body);

  //Draw lines
  for (let index = 0; index < srna_width; index = index + lineSeparation) {
    let line = canva
      .line(posX+index, dna.y, posX+index, dna.y - lineHeight)
      .stroke(stroke)
    srna.add(line);
  }

  //Draw label
  let text = label({
    canvas: canva,
    x: posX,
    element_y: posY,
    element_h: bodyHeight,
    element_w: srna_width,
    text: labelName,
    font: font
  });

  //Strand effect

  if(strand === "reverse"){
    posY = height + posY;
    if (anchor) {
      posX = srna.x;
      posY = dna.y + separation;
    }
    srna.transform({
      rotate: 180,
      translateY: height
    });
    text.move(text.x(),posY+separation*2+srna_dp.height);
    
  }

  //Actions
  if (onClick) {
    srna.attr({
      cursor: "pointer"
    })
    srna.click(onClick);
  }

  //srna.add(text);
  // Tooltip
  srna.attr({
    "data-tip": "",
    "data-for": `"${canva.node?.id}-${id}"`
  });
  return {
    id: id,
    canva: canva,
    draw: srna,
    posX: posX,
    posY: posY,
    srna_width: srna_width,
    height: height,
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
    objectType: "rna",
    tooltip: tooltip
  };
}
