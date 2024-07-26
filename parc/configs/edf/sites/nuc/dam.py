from parc.types import Site
from parc.constants import UnitTechnology
from parc.configs.edf.types import FrenchNuclearUnit
from parc.configs.edf.constants import FrenchNuclearUnitLevel


# DAMPIERRE
DAM = Site(
    name="dam",
    units=[
        FrenchNuclearUnit(
            name="dam" + str(i + 1),
            technology=UnitTechnology.NUCLEAR,
            level=FrenchNuclearUnitLevel.CP1,
        )
        for i in range(4)
    ],
)
