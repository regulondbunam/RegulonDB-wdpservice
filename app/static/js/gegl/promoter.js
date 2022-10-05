// Promoter 0.10.0
/**
 *
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import { label } from "./label.js";
import { promoter_dp } from "./features_default_properties/index.js";

export default function DrawPromoter({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 10,
  rightEndPosition = 50,
  labelName = "Name",
  strand = "forward",
  color,
  objectRGBColor,
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
  if (objectRGBColor) {
    color = objectRGBColor;
  }
  stroke = stroke_validate(stroke, promoter_dp.stroke);
  font = font_validate(font, promoter_dp.font);
  color = color_validate(color, "#000");
  //anchor
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  // attributes
  if (separation > 0) {
    height = 10
  }
  let promoter = canva.group();
  const promoter_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  let sizeP = (promoter_dp.width * dna.widthActive) / dna.size;
  if (sizeP > promoter_dp.width) {
    sizeP = promoter_dp.width;
  }
  //Body attributes
  let bodyH = height + separation;
  let bodyW = sizeP;
  const headH = promoter_dp.height;
  const draw_height = headH + bodyH;
  let posX = promoter_x + dna.x;
  let posY = dna.y;
  // Row attributes
  let pmX = posX + bodyW;
  let pmY = posY - bodyH;
  let az;
  // position
  let txtPosX = posX
  let txtPosY = posY - bodyH - font.size - 2
  let body = undefined
  if (strand === "reverse") {
    body = canva.path(
      "M " + posX + "," + posY + " v " + bodyH + " h -" + bodyW
    );
    txtPosX = posX - bodyW;
    txtPosY = posY + bodyH
    pmX = posX - bodyW;
    pmY = posY + bodyH;
    az = -5;
  } else {
    body = canva.path(
      "M " + posX + "," + posY + " v -" + bodyH + " h " + bodyW
    );
    az = 5;
  }

  // draw body
  body.fill("none");
  body.stroke(stroke);
  promoter.add(body);

  //text
  label({
    canvas: canva,
    x: txtPosX,
    y: txtPosY,
    text: labelName,
    font: font
  });

  // draw arrow
  const arrow = canva.path(
    "M " +
    (pmX - az) +
    "," +
    (pmY + az) +
    " " +
    pmX +
    "," +
    pmY +
    " " +
    (pmX - az) +
    "," +
    (pmY - az)
  );
  arrow.fill("none");
  arrow.stroke(stroke);
  promoter.add(arrow);
  //Actions
  promoter.opacity(opacity);
  if (onClick) {
    promoter.attr({
      cursor: "pointer"
    })
    promoter.click(onClick);
  }
  // Tooltip
  promoter.attr({
    "data-tip": tooltip,
    "data-for": `"${canva.node?.id}-${id}"`
  });

  return {
    id: id,
    canva: canva,
    width: 1,
    draw: promoter,
    posX: posX,
    posY: posY,
    height: draw_height,
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
    objectType: "promoter",
    tooltip: tooltip
  };
}
