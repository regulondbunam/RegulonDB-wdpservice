// TransAtt 0.10.0
/** transnationalAttenuator
 *
 *
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
//import { label } from "./label";
import { transnationalAttenuator_dp } from "./features_default_properties/index.js";

export default function DrawTransnationalAttenuator({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 10,
  labelName = "geneName",
  strand = "forward",
  color = "aqua",
  opacity = 1,
  stroke ={},
  font = {},
  tooltip = "",
  onClick
}) {
  if (!canva || !dna || !id || leftEndPosition > rightEndPosition) {
    return null;
  }
  stroke = stroke_validate(stroke, transnationalAttenuator_dp.stroke);
  font = font_validate(font, transnationalAttenuator_dp.font);
  color = color_validate(color, "#00FFFF");
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 1;
    strand = anchor.strand;
  }
  //attributes
  const transnationalAttenuator_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  let sizeP = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  //scale
  const proportion = transnationalAttenuator_dp.height;
  //Body attributes
  let bodyHeight = proportion * 3 + separation;
  let bodyFootH = proportion / 4;
  let bodyFootW = 0;
  if (sizeP >= proportion) {
    bodyFootW = sizeP / 2 - proportion / 3;
  }
  let bodyX = transnationalAttenuator_x + dna.x;
  let bodyY = dna.y - bodyHeight - bodyFootH;
  //atributos de Cabeza
  let headH = proportion;
  let headX = dna.x + transnationalAttenuator_x + sizeP / 2 - headH / 2;
  let headY = dna.y - bodyHeight - headH;
  // atributos del rectangulo
  let rectWidth = proportion / 2;
  let rectHeight = proportion * 2;
  let rectX = dna.x + transnationalAttenuator_x + sizeP - bodyFootW;
  let rectY = dna.y - bodyHeight;
  let posX = transnationalAttenuator_x;
  let posY = headY;
  let traH = headH + bodyHeight;
  // anchor effect
  if (anchor) {
  }
  // draw body
  const body = canva.path(
    "M 0,0 v " +
      bodyHeight +
      " h -" +
      bodyFootW +
      " v " +
      bodyFootH +
      " h " +
      sizeP +
      " v -" +
      bodyFootH +
      " h -" +
      bodyFootW +
      " v " +
      -bodyHeight
  );
  body.fill(color).move(bodyX, bodyY);
  body.stroke(stroke);
  body.opacity(opacity);
  // head draw
  const head = canva.circle(headH);
  head.fill(color).move(headX, headY);
  head.stroke(stroke);
  head.opacity(opacity);
  // rect draw
  const rect = canva.rect(rectWidth, rectHeight);
  rect.fill(color).move(rectX, rectY);
  rect.stroke(stroke);
  // reverse effect
  let group = canva.group();
  group.add(body);
  group.add(head);
  group.add(rect);
  if (strand === "reverse") {
    group.transform({
      rotate: 180,
      translateY: bodyHeight + headH + 1
    });
  }
  //Actions
  if (onClick) {
    group.attr({
      cursor: "pointer"
    })
    group.click(onClick);
  }
  group.attr({
    "data-tip": "",
    "data-for": `"${canva.node?.id}-${id}"`
  });
  //returns :C
  return {
    id: id,
    canva: canva,
    draw: group,
    posX: posX,
    posY: posY,
    sizeP: sizeP,
    height: traH,
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
    objectType: "transnational_attenuator",
    tooltip: tooltip
  };
}
