from array import array
from ..Citations import Citations
from ..Gene import ExternalCrossReferences
from ..GeneOntologyTerms import GeneOntologyTerms
from .Motifs import Motifs

Products = {
    "anticodon": str,
    "cellularLocations": [str],
    "citations": [Citations],
    "externalCrossReferences": [ExternalCrossReferences],
    "geneOntologyTerms": GeneOntologyTerms,
    "id": str,
    "isRegulator": bool,
    "isoelectricPoint": float,
    "molecularWeight": str,
    "motifs": [Motifs],
    "name": str,
    "note": str,
    "regulonId": str,
    "sequence": str,
    "synonyms": [str],
    "type": str,
}