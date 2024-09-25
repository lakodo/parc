from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

CHOOZ = Site(
    name="Chooz",
    units=[
        CHO1 := FrenchNuclearUnit(name="cho1", design=FrenchNuclearUnitDesign.N4),
        CHO2 := FrenchNuclearUnit(name="cho2", design=FrenchNuclearUnitDesign.N4),
    ],
)
