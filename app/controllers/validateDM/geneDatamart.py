from .Citations import Citations
from .Gene import Gene
from .Products import Products
from .Regulation import Regulation

geneDatamart = {
    "_id": str,
    "allCitations": [Citations],
    "gene": Gene,
    "products": [Products],
    "regulation": Regulation
}

#"growthConditions": [GrowthConditions]