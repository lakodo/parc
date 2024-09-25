from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.france import FRENCH_GRID
from parc.configs.edf.sites.nuc.belleville import BEL1
from parc.configs.edf.types import FrenchNuclearUnit
from parc.constants import UnitTechnology

# Example of one site
print("About", BEL1)
print("name:", BEL1.name, "\npower:", BEL1.power, "\ndesign", BEL1.design)

print("\n\n\n")

# Example over all units of a specific grid
for site in FRENCH_GRID.sites:
    print("-", site)
    for unit in site.units:
        if unit.technology == UnitTechnology.NUCLEAR:
            print("\t-", unit)

print("\n\n\n")

print(f"French 900: {len(FrenchNuclearUnit.get_900())} units")
print(f"French 1300: {len(FrenchNuclearUnit.get_1300())} units")
print(f"French 1450: {len(FrenchNuclearUnit.get_1450())} units")
print(f"French 1600: {len(FrenchNuclearUnit.get_1600())} units")

print("\n\n\n")

total = 0
for design in FrenchNuclearUnitDesign:
    total += (len_design := len(FrenchNuclearUnit.get_of_design(design)))
    print(f"French {design}: {len_design} units")

print("\n\n\n")

print("TOTAL:", total)

# TODO
# FLA1.ecs.rf.ASG021EC1

# FLA1.("ASG021EC1")
