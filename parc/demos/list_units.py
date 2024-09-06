from parc.configs.edf.france import FRENCH_GRID
from parc.configs.edf.sites.nuc.fla import FLA1
from parc.constants import UnitTechnology

# Example of one site
print(FLA1.name)


# Example over all units of a specific grid
for site in FRENCH_GRID.sites:
    print("-", site)
    for unit in site.units:
        if unit.technology == UnitTechnology.NUCLEAR:
            print("\t-", unit)

# TODO
# FLA1.ecs.rf.ASG021EC1

# FLA1.("ASG021EC1")
