from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

CIVAUX = Site(
    name="Civaux",
    units=[
        CIV1 := FrenchNuclearUnit(name="civ1", design=FrenchNuclearUnitDesign.N4),
        CIV2 := FrenchNuclearUnit(name="civ2", design=FrenchNuclearUnitDesign.N4),
    ],
)
