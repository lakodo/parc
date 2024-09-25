from parc.configs.edf.france import FRENCH_GRID
from parc.configs.edf.sites.nuc.belleville import BEL1
from parc.configs.edf.types import FrenchNuclearUnit
from parc.constants import UnitTechnology

# Example of one site
print("About", BEL1)
print("name:", BEL1.name, "\npower:", BEL1.power, "\ndesign", BEL1.design)


# Example over all units of a specific grid
for site in FRENCH_GRID.sites:
    print("-", site)
    for unit in site.units:
        if unit.technology == UnitTechnology.NUCLEAR:
            print("\t-", unit)


# Get all 900 French Nuclear Units
UNIT_900 = FrenchNuclearUnit.get_900()
print("French 900:s")
for unit in UNIT_900:
    print("\t-", unit)


# TODO
# FLA1.ecs.rf.ASG021EC1

# FLA1.("ASG021EC1")
