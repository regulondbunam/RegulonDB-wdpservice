//Draw Sites v 0.10.0
/**
 * Falta etiqueta
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import {tfBindingSite_dp} from './features_default_properties/index.js'
import { label } from "./label.js";

export default function DrawTfBindingSite({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 10,
  labelName = "Name",
  strand = "forward",
  color = "#fff",
  objectRGBColor,
  opacity = 1,
  stroke = {},
  font = {},
  height,
  tooltip = "",
  onClick
}) {
  if (!canva || !dna || !id | (leftEndPosition > rightEndPosition)) {
    return null;
  }
  if (objectRGBColor) {
    color = objectRGBColor;
  }
  stroke = stroke_validate(stroke, tfBindingSite_dp.stroke);
  font = font_validate(font, tfBindingSite_dp.font);
  color = color_validate(color, "#00FFFF");
  // anchor effect
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  //attributes
  const tfBindingSite_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  let tfBindingSite_width = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  if(tfBindingSite_width > 100){
    tfBindingSite_width = ((30) * dna.widthActive) / dna.size;
  }
  const group = canva.group();
  
  // scale
  let proportion = tfBindingSite_dp.height;
  if (height) {
    proportion = height;
  }  
  //body attributes
  let tfH = proportion;
  let tfW = tfBindingSite_width;
  let posX = tfBindingSite_x + dna.x;
  let posY = dna.y - separation - tfH;
  //Draw SITES
  let tf_binding = canva.rect(tfW, tfH);
  tf_binding.move(posX, posY).stroke(stroke).fill(color);
  //Text properties
  group.add(tf_binding);
  if(tfW > (tfH*font.size/25)*labelName.length){
    let textP = label({
      text: labelName,
      id: id + "_label",
      canvas: canva,
      element_x: posX,
      element_y: posY,
      element_w: tfW,
      element_h: tfH,
      font: font,
      size: tfH*font.size/25
    })
  group.add(textP);
  }
  
  //opacity
  group.opacity(opacity);
  //strand effect
  if (strand === "reverse") {
    posY = dna.y + separation;
    group.move(posX, posY);
  }
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
    tfBindingSite_width: tfBindingSite_width,
    height: tfH,
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
    objectType: "tf_binding_site",
    tooltip: tooltip
  };
}
