from ..Citations import Citations
from .ExternalCrossReferences import ExternalCrossReferences
from .Fragments import Fragments
from .MultifunTerms import MultifunTerms

Gene = {
    "bnumber": str,
    "centisomePosition": float,
    "citations": [Citations],
    "externalCrossReferences": [ExternalCrossReferences],
    "fragments": [Fragments],
    "gcContent": float,
    "id": str,
    "leftEndPosition": int,
    "multifunTerms": [MultifunTerms],
    "name": str,
    "note": str,
    "rightEndPosition": int,
    "sequence": str,
    "strand": str,
    "synonyms": [str],
    "type": str
}