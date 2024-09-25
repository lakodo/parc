from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

PALUEL = Site(
    name="Paluel",
    units=[
        FrenchNuclearUnit(
            name="bla" + str(i + 1),
            design=FrenchNuclearUnitDesign.P4,
        )
        for i in range(4)
    ],
)
