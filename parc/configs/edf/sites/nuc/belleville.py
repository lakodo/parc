from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

BELLEVILLE = Site(
    name="Belleville-sur-Loire",
    units=[
        BEL1 := FrenchNuclearUnit(name="bel1", design=FrenchNuclearUnitDesign.PP4),
        BEL2 := FrenchNuclearUnit(name="bel2", design=FrenchNuclearUnitDesign.PP4),
    ],
)
