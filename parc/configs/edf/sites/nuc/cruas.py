from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

CRUAS = Site(
    name="Cruas",
    units=[
        CRU1 := FrenchNuclearUnit(name="cru1", design=FrenchNuclearUnitDesign.CP1),
        CRU2 := FrenchNuclearUnit(name="cru2", design=FrenchNuclearUnitDesign.CP1),
        CRU3 := FrenchNuclearUnit(name="cru3", design=FrenchNuclearUnitDesign.CP1),
        CRU4 := FrenchNuclearUnit(name="cru4", design=FrenchNuclearUnitDesign.CP1),
    ],
)
