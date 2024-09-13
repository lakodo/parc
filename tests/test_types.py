import contextlib

from parc import types
from parc.constants import UnitTechnology
from parc.types.errors.setting_errors import UniqueUnitError


def test_types():
    some_nuclear_unit = types.Unit(name="my first nuclear unit", technology=UnitTechnology.NUCLEAR)
    some_site = types.Site(name="some site", units=[some_nuclear_unit])
    print(some_site)  # uses the __repr__

    the_grid = types.Grid(name="the grid", sites=[some_site])

    with contextlib.suppress(UniqueUnitError):
        types.Unit(name="my first nuclear unit", technology=UnitTechnology.NUCLEAR)

    types.Grid(name="the empty grid")  # no units
    assert the_grid.sites[0].units[0].name == some_nuclear_unit.name
