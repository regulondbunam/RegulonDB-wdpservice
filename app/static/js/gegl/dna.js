//draw DNA v 0.11.0
/**
 * Requiere documetacion y encabezados del manifiesto de RegulonDB
 * 
 */
import { stroke_validate, font_validate } from "./validation/index.js";
import { dna_dp } from "./features_default_properties/index.js";


export default function DrawDna({
  id,
  canva,
  x = 0,
  y = 150,
  leftEndPosition = 800,
  rightEndPosition = 1000,
  labelName,
  opacity = 1,
  stroke = {},
  font = {},
  tooltip = ""
}) {
  //validation
  if (!canva || !id) {
    return null;
  }
  stroke = stroke_validate(stroke, dna_dp.stroke);
  font = font_validate(font, dna_dp.font);
  //labels attributes
  const dnaLletter = `${leftEndPosition}`;
  const dnaRletter = `${rightEndPosition}`;
  //DNA attributes
  const canvaW = canva.node.clientWidth;
  const lx1 = x + (font["size"] * dnaLletter.length) / 2 + 5;
  const lx2 = canvaW - (font["size"] * dnaRletter.length) / 2 - 7;
  const widthActive = lx2 - lx1;
  //console.log(canva.node.clientHeight)
  const forwardActive = y;
  const reverseActive = canva.node.clientHeight - y - stroke.width;
  //draw text
  if (labelName) {
    canva
      .text(labelName)
      .font(font)
      .move(lx2 - font["size"] / 2, 1);
  }

  canva
    .text(dnaLletter)
    .font(font)
    .move(x, y - font["size"] / 2);
  canva
    .text(dnaRletter)
    .font(font)
    .move(
      canvaW - (font["size"] * dnaRletter.length) / 2 - 2,
      y - font["size"] / 2
    );
  //draw dna
  const dna = canva.line(lx1, y, lx2, y).stroke(stroke).opacity(opacity);
  //return
  return {
    id: id,
    canva: canva,
    draw: dna,
    x: lx1,
    y: y,
    widthActive: widthActive,
    forwardActive: forwardActive,
    reverseActive: reverseActive,
    leftEndPosition: leftEndPosition,
    rightEndPosition: rightEndPosition,
    size: rightEndPosition - leftEndPosition,
    labelName: labelName,
    opacity: opacity,
    stroke: stroke,
    font: font,
    tooltip: tooltip,
    objectType: "dna"
  };
}
