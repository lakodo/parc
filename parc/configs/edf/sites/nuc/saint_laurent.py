from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

SAINT_LAURENT = Site(
    name="Saint Laurent",
    units=[
        FrenchNuclearUnit(
            name="sla" + str(i + 1),
            design=FrenchNuclearUnitDesign.CP1,
        )
        for i in range(2)
    ],
)
