// default properties
const dna_dp = {
  objectType: "dna",
  defaultColor: "#EFEBEB",
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 0,
};
const gene_dp = {
  objectType: "gene",
  height: 40,
  rowSize: 0.5,
  color: "#EFEBEB",
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 1,
  verticalPriority: 1,
};
const operon_dp = {
  objectType: "operon",
  defaultColor: "#EFEBEB",
  height: 40,
  rowSize: 0.5,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 2,
  verticalPriority: 1,
};
const ppgpp_dp = {
  objectType: "ppGpp",
  defaultColor: "#EFEBEB",
  height: 40,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 6,
    family: "arial",
    fill: "#000",
    weight: "bold",
  },
  drawPriority: 10,
  verticalPriority: 4,
};
const promoter_dp = {
  objectType: "promoter",
  defaultColor: "#000",
  height: 41,
  width: 20,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 3,
  verticalPriority: 3,
};
const riboswitch_dp = {
  objectType: "riboswitch",
  defaultColor: "#EFEBEB",
  height: 40,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 4,
  verticalPriority: 3,
};
const srna_dp = {
  objectType: "srna",
  defaultColor: "#EFEBEB",
  height: 20,
  lineSeparation: 5,
  fill: "#aaaaaa",
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 8,
  verticalPriority: 2,
};
const terminator_dp = {
  objectType: "terminator",
  defaultColor: "#EFEBEB",
  height: 50,
  proportions: {
    head: 0.2,
    body: 0.7,
    foot: 0.1,
  },
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 7,
  verticalPriority: 3,
};
const tfBindingSite_dp = {
  objectType: "tf_binding_site",
  defaultColor: "#EFEBEB",
  height: 20,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 11,
  verticalPriority: 2,
};
const transcriptionalAttenuator_dp = {
  objectType: "transcriptional_tf_binding_site",
  defaultColor: "#EFEBEB",
  height: 30,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 5,
  verticalPriority: 3,
};
const transnationalAttenuator_dp = {
  objectType: "translational_tf_binding_site",
  defaultColor: "#EFEBEB",
  height: 30,
  stroke: { color: "#000", width: 1, linecap: "round" },
  font: {
    size: 12,
    family: "arial",
    fill: "#000",
  },
  drawPriority: 6,
  verticalPriority: 3,
};

const dnaObjects_list = [
  gene_dp.objectType,
  operon_dp.objectType,
  ppgpp_dp.objectType,
  promoter_dp.objectType,
  riboswitch_dp.objectType,
  srna_dp.objectType,
  terminator_dp.objectType,
  tfBindingSite_dp.objectType,
  transcriptionalAttenuator_dp.objectType,
  transnationalAttenuator_dp.objectType,
  dna_dp.objectType,
];

function getPropertiesByObjectType(objectType) {
  switch (objectType) {
    case gene_dp.objectType:
      return gene_dp;
    case operon_dp.objectType:
      return operon_dp;
    case ppgpp_dp.objectType:
      return ppgpp_dp;
    case promoter_dp.objectType:
      return promoter_dp;
    case riboswitch_dp.objectType:
      return riboswitch_dp;
    case srna_dp.objectType:
      return srna_dp;
    case terminator_dp.objectType:
      return terminator_dp;
    case tfBindingSite_dp.objectType:
      return tfBindingSite_dp;
    case transcriptionalAttenuator_dp.objectType:
      return transcriptionalAttenuator_dp;
    case transnationalAttenuator_dp.objectType:
      return transnationalAttenuator_dp;
    case dna_dp.objectType:
      return dna_dp;
    default:
      return undefined;
  }
}

export {
  dnaObjects_list,
  getPropertiesByObjectType,
  dna_dp,
  gene_dp,
  operon_dp,
  ppgpp_dp,
  promoter_dp,
  riboswitch_dp,
  srna_dp,
  terminator_dp,
  tfBindingSite_dp,
  transcriptionalAttenuator_dp,
  transnationalAttenuator_dp,
};
