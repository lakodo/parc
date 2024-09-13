from parc.configs.edf.constants import FrenchNuclearUnitLevel
from parc.configs.edf.types import FrenchNuclearUnit
from parc.constants import UnitTechnology
from parc.types import Site

# GRAVELINES
GRA = Site(
    name="gra",
    units=[
        FrenchNuclearUnit(
            name="gra" + str(i + 1),
            technology=UnitTechnology.NUCLEAR,
            level=FrenchNuclearUnitLevel.CP1,
        )
        for i in range(6)
    ],
)
