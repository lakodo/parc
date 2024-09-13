from parc.types.errors.setting_errors import UniqueUnitError


def test_UniqueUnitError():
    UniqueUnitError(unit="a unit")
