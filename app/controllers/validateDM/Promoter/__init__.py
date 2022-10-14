from ..Citations import Citations
from .BindsSigmaFactor import BindsSigmaFactor
from .Boxes import Boxes
from ..RegulatorBindingSites import RegulatorBindingSites
from .TranscriptionStartSite import TranscriptionStartSite

Promoter = {
"bindsSigmaFactor": BindsSigmaFactor,
"boxes": [Boxes],
"citations": [Citations],
"id": str,
"name": str,
"note": str,
"regulatorBindingSites": [RegulatorBindingSites],
"score": str,
"sequence": str,
"synonyms": [str],
"transcriptionStartSite": TranscriptionStartSite
}