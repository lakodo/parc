from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

GOLFECH = Site(
    name="Golfech",
    units=[
        FrenchNuclearUnit(name="gol1", design=FrenchNuclearUnitDesign.PP4),
        FrenchNuclearUnit(name="gol2", design=FrenchNuclearUnitDesign.PP4),
    ],
)
