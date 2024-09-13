from parc.configs.edf.constants import FrenchNuclearUnitLevel
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

# DAMPIERRE
DAM = Site(
    name="dam",
    units=[
        FrenchNuclearUnit(
            name="dam" + str(i + 1),
            level=FrenchNuclearUnitLevel.CP1,
        )
        for i in range(4)
    ],
)
