//DrawOperon v 0.10.0
/**
 *falta agregar la funcion para mostrar el corte del elemento
 * 
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import { label } from "./label.js";
import { operon_dp } from "./features_default_properties/index.js";

export default function DrawOperon({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 20,
  labelName = "operonName",
  strand = "forward",
  color = "aqua",
  opacity = 1,
  stroke = {},
  font = {},
  height,
  tooltip = "",
  onClick
}) {
  //validation
  if (!canva || !dna || !id || leftEndPosition > rightEndPosition) {
    return null;
  }
  stroke = stroke_validate(stroke, operon_dp.stroke);
  font = font_validate(font, operon_dp.font);
  color = color_validate(color, "#00FFFF");
  //anchor
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  //Operon attributes
    const operon_x = ((leftEndPosition - dna.leftEndPosition) * dna?.widthActive) / dna.size;
    const operon_width = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  // separation
  if (strand === "reverse") {
    separation *= -1;
  }
  //body attributes
  if (!height) {
    height = operon_dp.height;
  }
  const rowW = () => {
    return height * operon_dp?.rowSize;
  };
  const lx1 = operon_width + dna.x + operon_x;
  const ly1 = height;
  const lx2 = operon_width + dna.x - rowW() + operon_x;
  let posX = operon_x + dna.x;
  let posY = dna.y - separation - height;
  //Draw operon

  const operon = canva.path(
    "m " +
      (operon_x + dna.x) +
      "," +
      height / 2 +
      " v " +
      height +
      " h " +
      (operon_width - rowW()) +
      " L " +
      lx1 +
      "," +
      ly1 +
      " " +
      lx2 +
      "," +
      height / 2 +
      " z"
  );
  operon.move(posX, posY);
  operon.id(id);
  operon.fill(color);
  operon.stroke(stroke);
  operon.opacity(opacity);
  
  //Draw label
  const text = label({
    canvas: canva,
    element_x: posX,
    element_y: posY,
    element_h: height,
    element_w: operon_width,
    text: labelName,
    font: font
  });
  // reverse effect
  if (strand === "reverse") {
    if (anchor) {
      posX = operon_x + dna.x;
      posY = dna.y + separation;
    }
    operon.transform({
      rotate: 180,
      translateY: height
    });
    text.transform({
      translateY: height
    });
    posY = height * 2 + posY;
  }
  //Actions
  if (onClick) {
    operon.attr({
      cursor: "pointer"
    })
    operon.click(onClick);
  }
  // Toltip
  //return
  return {
    id: id,
    canva: canva,
    draw: operon,
    posX: posX,
    posY: posY,
    width: operon_width,
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
    objectType: operon_dp?.objectType,
    tooltip: tooltip
  };
}
