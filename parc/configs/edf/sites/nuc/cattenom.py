from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

CATTENOM = Site(
    name="Cattenom",
    units=[
        CAT1 := FrenchNuclearUnit(name="cat1", design=FrenchNuclearUnitDesign.PP4),
        CAT2 := FrenchNuclearUnit(name="cat2", design=FrenchNuclearUnitDesign.PP4),
        CAT3 := FrenchNuclearUnit(name="cat3", design=FrenchNuclearUnitDesign.PP4),
        CAT4 := FrenchNuclearUnit(name="cat4", design=FrenchNuclearUnitDesign.PP4),
    ],
)
