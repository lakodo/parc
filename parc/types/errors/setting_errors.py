import typing


class UniqueUnitError(Exception):
    """This unit already exists"""

    def __init__(self, unit: typing.Any):
        super().__init__("This unit has already been set: " + str(unit))
