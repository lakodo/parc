from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

TRICASTIN = Site(
    name="Tricastin",
    units=[
        FrenchNuclearUnit(
            name="tri" + str(i + 1),
            design=FrenchNuclearUnitDesign.CP1,
        )
        for i in range(4)
    ],
)
