from ..Citations import Citations
from .RegulatorySite import RegulatorySite

RegulatoryInteractions = {
"_id": str,
"centerPosition": float,
"citations": [Citations],
"function": str,
"mechanism": str,
"note": str,
"regulatorySite": RegulatorySite
}