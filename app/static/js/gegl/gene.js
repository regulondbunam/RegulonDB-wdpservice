//DrawGene v 0.10.0
/**
 * falta agregar la funcion para mostrar el corte del elemento,
 */
import { stroke_validate, font_validate, color_validate } from "./validation/index.js";
import { label } from "./label.js";
import { gene_dp } from "./features_default_properties/index.js";


export default function DrawGene({
  id,
  canva,
  anchor,
  dna,
  separation = 0,
  leftEndPosition = 0,
  rightEndPosition = 20,
  labelName = "geneName",
  strand = "forward",
  color,
  objectRGBColor,
  opacity = 1,
  stroke = {},
  font = {},
  height,
  tooltip = "",
  onClick
}) {
  //Validation
  if (!canva || !dna || !id | (leftEndPosition > rightEndPosition)) {
    return null;
  }
  if(objectRGBColor){
    color = objectRGBColor;
  }
  stroke = stroke_validate(stroke, gene_dp.stroke);
  font = font_validate(font, gene_dp.font);
  color = color_validate(color, gene_dp.color);
  //anchor
  if (anchor) {
    leftEndPosition = anchor.leftEndPosition;
    rightEndPosition = leftEndPosition + 10;
  }
  //gene attributes
  const
    gene_x = ((leftEndPosition - dna.leftEndPosition) * dna.widthActive) / dna.size,
    gene_width = ((rightEndPosition - leftEndPosition) * dna.widthActive) / dna.size;
  // separation
  if (strand === "reverse") {
    separation *= -1;
  }
  //body attributes
  if (!height) {
    height = gene_dp.height;
  }
    
  const proportion = height / gene_dp.height;
  const body_height = 20 * proportion;

  const rowW = () => {
    return body_height * gene_dp.rowSize;
  };
  //console.log(gene_x)
  const lx1 = gene_width + dna.x + gene_x;
  const ly1 = body_height;
  const lx2 = gene_width + dna.x - rowW() + gene_x;
  const ly2 = 0;
  let posX = gene_x + dna.x;
  let posY = dna.y - separation - body_height * 2;
  //Draw Gene
  const gene = canva.path(
    "m " +
    (gene_x + dna.x) +
    "," +
    body_height / 2 +
    " v " +
    body_height +
    " h " +
    (gene_width - rowW()) +
    " v " +
    body_height / 2 +
    " L " +
    lx1 +
    "," +
    ly1 +
    " " +
    lx2 +
    "," +
    ly2 +
    " v " +
    body_height / 2 +
    " z"
  );
  //console.log(posX);
  gene.move(posX, posY);
  gene.id(id);
  gene.fill(color);
  gene.stroke(stroke);
  gene.opacity(opacity);
  //label
  const text = label({
    canvas: canva,
    element_x: posX,
    element_y: posY + body_height / 2,
    element_h: body_height,
    element_w: gene_width,
    text: labelName,
    font: font
  });
  // reverse effect
  if (strand === "reverse") {
    if (anchor) {
      posX = gene.x;
      posY = dna.y + separation;
    }
    gene.transform({
      rotate: 180,
      translateY: body_height * 2
    });
    text.transform({
      translateY: body_height * 2
    });
    posY = body_height * 2 + posY;
  }
  //Actions
  if (onClick) {
    gene.attr({
      cursor: "pointer"
    })
    gene.click(onClick);
  }
  // Tooltip
  

  return {
    id: id,
    canva: canva,
    draw: gene,
    posX: posX,
    posY: posY,
    width: gene.width,
    body_height: body_height,
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
    objectType: gene_dp.objectType,
    tooltip: tooltip
  };
}
