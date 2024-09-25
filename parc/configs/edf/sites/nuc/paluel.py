from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

PALUEL = Site(
    name="Paluel",
    units=[
        FrenchNuclearUnit(name="pal1", design=FrenchNuclearUnitDesign.P4),
        FrenchNuclearUnit(name="pal2", design=FrenchNuclearUnitDesign.P4),
        FrenchNuclearUnit(name="pal3", design=FrenchNuclearUnitDesign.P4),
        FrenchNuclearUnit(name="pal4", design=FrenchNuclearUnitDesign.P4),
    ],
)
