from .belleville import BELLEVILLE

FRENCH_NUCLEAR_SITES = [BELLEVILLE]
FRENCH_NUCLEAR_UNITS = [unit for site in FRENCH_NUCLEAR_SITES for unit in site.units]
FRENCH_NUCLEAR_PRODUCING_UNITS = [
    unit for site in FRENCH_NUCLEAR_SITES for unit in site.units if unit.electricity_producer
]

__all__ = ["FRENCH_NUCLEAR_SITES", "FRENCH_NUCLEAR_UNITS", "FRENCH_NUCLEAR_PRODUCING_UNITS"]