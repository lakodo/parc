from parc.configs.edf.sites.nuc.fla import FLA1
from parc.configs.edf.france import FRENCH_GRID

print(FLA1.name)

for site in FRENCH_GRID.sites:
    print("-",site)
    for unit in site.units:
        print("\t-",unit)
