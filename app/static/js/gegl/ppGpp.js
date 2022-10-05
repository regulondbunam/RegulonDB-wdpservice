//DrawPpGpp v 0.10.0

import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import { label } from "./label.js";
import { ppgpp_dp } from "./features_default_properties/index.js";

export default function DrawPpGpp({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 10,
  labelName = "ppGpp",
  strand = "forward",
  color = "#AFAFAF",
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
  stroke = stroke_validate(stroke, ppgpp_dp.stroke);
  font = font_validate(font, ppgpp_dp.font);
  color = color_validate(color, "#AFAFAF");
  // anchor
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  // attributes
  const ppgpp_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  // body attributes
  if (!height) {
    height = ppgpp_dp.height;
  }
  let ell_w = font.size * 4;
  let ell_h = font.size + 10;
  let posX = ppgpp_x + dna.x;
  let posY = dna.y - separation - height / 2 - ell_h / 2;
  if (strand === "reverse") {
    posY = dna.y + separation + height / 2 - ell_h / 2;
  }
  //Draw
  if (labelName === "DksA-ppGpp") {
    canva
      .ellipse(ell_w + 3, ell_h + 2)
      .move(posX, posY)
      .stroke(stroke)
      .fill(color);
    font.size += 2;
    label({
      canvas: canva,
      element_x: posX,
      element_y: posY,
      element_h: ell_h,
      element_w: ell_w,
      text: "DksA",
      font: font
    });
    font.size -= 2;
    posX += ell_w - 1;
  }
  canva.ellipse(ell_w, ell_h).move(posX, posY).stroke(stroke).fill(color);
  label({
    canvas: canva,
    element_x: posX,
    element_y: posY,
    element_h: ell_h,
    element_w: ell_w,
    text: "ppGpp",
    font: font
  });
  const group = canva.group();
  group.opacity(opacity);
  //Actions
  if (onClick) {
    group.attr({
      cursor: "pointer"
    })
    group.click(onClick);
  }
  // Toltip
  group.attr({
    "data-tip": "",
    "data-for": `"${canva.node?.id}-${id}"`
  });

  return {
    id: id,
    canva: canva,
    posX: posX,
    posY: posY,
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
    objectType: "ppGpp",
    tooltip: tooltip
  };
}
