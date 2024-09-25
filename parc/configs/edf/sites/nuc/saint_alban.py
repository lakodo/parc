from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

SAINT_ALBAN = Site(
    name="Saint Alban",
    units=[
        FrenchNuclearUnit(name="sal1", design=FrenchNuclearUnitDesign.P4),
        FrenchNuclearUnit(name="sal2", design=FrenchNuclearUnitDesign.P4),
    ],
)
