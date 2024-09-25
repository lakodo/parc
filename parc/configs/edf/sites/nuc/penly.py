from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

PENLY = Site(
    name="Penly",
    units=[
        FrenchNuclearUnit(name="pen1", design=FrenchNuclearUnitDesign.PP4),
        FrenchNuclearUnit(name="pen2", design=FrenchNuclearUnitDesign.PP4),
    ],
)
