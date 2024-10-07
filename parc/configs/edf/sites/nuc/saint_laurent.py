from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

SAINT_LAURENT = Site(
    name="Saint Laurent",
    units=[
        FrenchNuclearUnit(
            name="slb" + str(i + 1),
            design=FrenchNuclearUnitDesign.CP2,
        )
        for i in range(2)
    ],
)
