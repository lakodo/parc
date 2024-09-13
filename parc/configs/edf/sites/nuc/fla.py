from parc.configs.edf.constants import FrenchNuclearUnitLevel
from parc.configs.edf.types import FrenchNuclearUnit
from parc.constants import UnitTechnology
from parc.types import Site

# FLAMANVILLE
FLA1 = FrenchNuclearUnit(name="fla1", technology=UnitTechnology.NUCLEAR, level=FrenchNuclearUnitLevel.P4)
FLA2 = FrenchNuclearUnit(name="fla2", technology=UnitTechnology.NUCLEAR, level=FrenchNuclearUnitLevel.P4)
FLA3 = FrenchNuclearUnit(name="fla3", technology=UnitTechnology.NUCLEAR, level=FrenchNuclearUnitLevel.EPR)
FLA = Site(name="fla", units=[FLA1, FLA2, FLA3])
