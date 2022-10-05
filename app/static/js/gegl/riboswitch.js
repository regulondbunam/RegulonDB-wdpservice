/** RiboSwitch 0.10.0
 *
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import { label } from "./label.js";
import { riboswitch_dp } from "./features_default_properties/index.js";

export default function DrawRiboswitch({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 100,
  labelName = "",
  strand = "forward",
  color,
  opacity = 1,
  stroke = {},
  font = {},
  tooltip = "",
  onClick
}) {
  if (!canva || !dna || !id | (leftEndPosition > rightEndPosition)) {
    return null;
  }
  stroke = stroke_validate(stroke, riboswitch_dp.stroke);
  font = font_validate(font, riboswitch_dp.font);
  let fill_opacity = 1;
  if (!color) {
    fill_opacity = 0;
  }
  color = color_validate(color, "#00FFFF");
  // anchor effect
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  //attributes

  const rb_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size;
  let rb_width = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  const proportion = riboswitch_dp.height / 40;

  // Body attributes

  let bodyHeight = proportion * 15 + separation;
  let bodyFootH = proportion * 5;
  let bodyFootW = 0;
  if (rb_width >= 10 * proportion) {
    bodyFootW = rb_width / 2 - (proportion * 9) / 2;
  }
  let bodyX = rb_x + dna.x;
  let bodyY = dna.y - bodyHeight - bodyFootH;

  //Head attributes
  let headHeight = proportion * 10;
  //let headWidth = proportion * 30;
  let height = bodyHeight + bodyFootH + headHeight;

  //Draw Body
  const body = canva.path(
    "M 0,0 v " +
    bodyHeight +
    " h -" +
    bodyFootW +
    " v " +
    bodyFootH +
    " h " +
    rb_width +
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
  body.attr({
    "fill-opacity": fill_opacity
  });
  // draw label
  const text = label({
    canvas: canva,
    element_x: bodyX,
    element_y: bodyY - bodyHeight - headHeight * 2,
    element_h: height,
    element_w: rb_width,
    text: labelName,
    font: font
  });
  // draw head
  let headX = bodyX + bodyFootW + 10 * proportion;
  let headY = bodyY;
  // console.log(headX + "," + headY);
  const head = canva.path(
    "m " +
    headX +
    ", " +
    headY +
    " v 0 c 0,0 1.785875,-0.7713442 2.028104,-2.6543252 l 3.947824,-1.767943 c 0.61709,0.163879 1.275534,0.125563 1.866142,-0.10859 1.429117,-0.56887 2.094681,-2.113376 1.486692,-3.450008 -0.608282,-1.336907 -2.260344,-1.959428 -3.689789,-1.390364 -0.673801,0.26844 -1.209079,0.772083 -1.492011,1.403849 l -3.025745,1.251259 c -1.221776,-2.013757 -3.505187,-3.259375 -5.980932,-3.262641 v 0 c -2.580198,0.0024 -4.942473,1.353582 -6.1205615,3.5004 l -2.95593,-1.230676 c -0.03061,-0.100627 -0.06761,-0.199454 -0.110799,-0.295959 -0.608291,-1.336516 -2.259799,-1.958956 -3.689038,-1.390365 -1.42953114,0.56887 -2.09518574,2.113892 -1.48669174,3.450719 0.54125214,1.185023 1.92076374,1.828886 3.25873474,1.520954 l 4.003975,1.769365 c 0.26385,1.748466 2.1346045,2.5948372 2.1346045,2.5948372"
  );
  head.fill(color);
  head.stroke(stroke);
  head.opacity(opacity);
  head.attr({
    "fill-opacity": fill_opacity
  });
  head.transform({
    scale: proportion,
    translateX: -proportion,
    origin: "center"
  });
  let posX = rb_x + dna.x;
  let posY = dna.y - separation - bodyHeight;
  var rb = canva.group();
  rb.add(body);
  rb.add(head);

  //reverse effect
  if (strand === "reverse") {
    rb.transform({
      rotate: 180,
      translateY: height
    });
    text.transform({
      translateY: headHeight * 2 + height * 2
    });
    posY = bodyHeight + posY;
  }
  //Actions
  if (onClick) {
    rb.attr({
      cursor: "pointer"
    })
    rb.click(onClick);
  }
  // Tooltip
  rb.attr({
    "data-tip": "",
    "data-for": `"${canva.node?.id}-${id}"`
  });

  return {
    id: id,
    canva: canva,
    draw: rb,
    posX: posX,
    posY: posY,
    width: rb_width,
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
    objectType: "promoter",
    tooltip: tooltip
  };
}
