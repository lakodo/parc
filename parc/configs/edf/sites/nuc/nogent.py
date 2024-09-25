from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

NOGENT = Site(
    name="Nogent-sur-Seine",
    units=[
        FrenchNuclearUnit(name="nog1", design=FrenchNuclearUnitDesign.PP4),
        FrenchNuclearUnit(name="nog2", design=FrenchNuclearUnitDesign.PP4),
    ],
)
