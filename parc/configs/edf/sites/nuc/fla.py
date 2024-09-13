from parc.configs.edf.constants import FrenchNuclearUnitLevel
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

# FLAMANVILLE
FLA1 = FrenchNuclearUnit(name="fla1", level=FrenchNuclearUnitLevel.P4)
FLA2 = FrenchNuclearUnit(name="fla2", level=FrenchNuclearUnitLevel.P4)
FLA3 = FrenchNuclearUnit(name="fla3", level=FrenchNuclearUnitLevel.EPR)
FLA = Site(name="fla", units=[FLA1, FLA2, FLA3])
