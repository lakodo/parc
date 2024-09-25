from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

GRAVELINES = Site(
    name="Gravelines",
    units=[
        FrenchNuclearUnit(
            name="gra" + str(i + 1),
            design=FrenchNuclearUnitDesign.CP1,
        )
        for i in range(6)
    ],
)
