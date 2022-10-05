//import { font_validate, color_validate } from "./validation";

export function label({
  id,
  canvas,
  x,
  y,
  element_x,
  element_y,
  element_w,
  element_h,
  text = "",
  font,
  size,
}) {
  const label = canvas.text(text);
  if (size) {
    font.size = size;
  }
  label.font(font);
  if (!x) {
    x = element_x + element_w / 2 - label.length() / 2;
  }
  if (!y) {
    y = element_y + element_h / 2 - font.size / 2;
  }
  label.move(x, y);
  return label;
}

/*
({
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
  opacity = 1,
  stroke,
  font,
  tooltip = ""
}) {

*/
