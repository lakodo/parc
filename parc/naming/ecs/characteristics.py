"""Parsers for ECS characteristics associated with equipment and buildings."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .buildings import (
    FIRE_CODE_ORDER,
    FIRE_CRITERION_LABELS,
    FIRE_KIND_LABELS,
    LOCAL_CODE_LABELS,
    level_altitude_range,
    parse_building_trigram,
)
from .ecs import describe_ecs_code, normalize_ecs_code

LOCATION_REGEX = (
    r"(?P<tranche>[0-9])?"
    r"(?P<building>H[A-Z]{2})"
    r"(?P<identification>[0-9]{4})"
    r"Z(?P<kind>[ACLM])-"
)
LOCATION_PATTERN = re.compile(f"^{LOCATION_REGEX}$")
LOCATION_FINDER_PATTERN = re.compile(rf"(?<![A-Z0-9])(?P<value>{LOCATION_REGEX})(?![A-Z0-9])")

FIRE_REGEX = (
    r"(?P<tranche>[0-9])?"
    r"(?P<building>H[A-Z]{2})"
    r"(?P<identification>[0-9]{4})"
    r"(?P<kind>[SZ])F(?P<criterion>[CIS])"
)
FIRE_PATTERN = re.compile(f"^{FIRE_REGEX}$")
FIRE_FINDER_PATTERN = re.compile(rf"(?<![A-Z0-9])(?P<value>{FIRE_REGEX})(?![A-Z0-9])")

ELECTRICAL_SUPPLY_REGEX = (
    r"(?P<tranche>[0-9])?"
    r"(?P<system>L[A-Z]{2})"
    r"(?P<slot>[0-9][A-Z0-9][A-Z0-9][0-9])"
    r"JC-"
)
ELECTRICAL_SUPPLY_PATTERN = re.compile(f"^{ELECTRICAL_SUPPLY_REGEX}$")
ELECTRICAL_SUPPLY_FINDER_PATTERN = re.compile(
    rf"(?<![A-Z0-9])(?P<value>{ELECTRICAL_SUPPLY_REGEX})(?![A-Z0-9])"
)


def normalize_characteristic(value: str) -> str:
    """Normalize a characteristic code."""

    return value.strip().upper().replace(" ", "")


@dataclass(frozen=True)
class BuildingIdentification:
    """Shared interpretation of the 4-digit building identification section."""

    raw: str

    @property
    def level(self) -> str:
        return self.raw[:2]

    @property
    def sequence(self) -> str:
        return self.raw[2:]

    @property
    def altitude_range(self) -> tuple[float, float] | None:
        return level_altitude_range(self.level)


@dataclass(frozen=True)
class LocationReference:
    """ECS localisation characteristic."""

    tranche: str | None
    building: str
    identification: BuildingIdentification
    local_kind: str

    @property
    def code(self) -> str:
        return f"{self.tranche or ''}{self.building}{self.identification.raw}Z{self.local_kind}-"

    @property
    def building_label(self) -> str | None:
        return parse_building_trigram(self.building).family_label

    @property
    def local_kind_label(self) -> str | None:
        return LOCAL_CODE_LABELS.get(self.local_kind)

    @property
    def local_number(self) -> str:
        return self.identification.sequence

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class FireSectorReference:
    """ECS fire sectorisation characteristic."""

    tranche: str | None
    building: str
    identification: BuildingIdentification
    kind: str
    criterion: str

    @property
    def code(self) -> str:
        return f"{self.tranche or ''}{self.building}{self.identification.raw}{self.kind}F{self.criterion}"

    @property
    def building_label(self) -> str | None:
        return parse_building_trigram(self.building).family_label

    @property
    def kind_label(self) -> str | None:
        return FIRE_KIND_LABELS.get(self.kind)

    @property
    def criterion_label(self) -> str | None:
        return FIRE_CRITERION_LABELS.get(self.criterion)

    @property
    def sector_number(self) -> str:
        return self.identification.sequence

    @property
    def rank(self) -> int | None:
        try:
            return FIRE_CODE_ORDER.index(f"{self.kind}F{self.criterion}")
        except ValueError:
            return None

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class ElectricalSupplyReference:
    """ECS electrical supply characteristic."""

    tranche: str | None
    system: str
    slot: str

    @property
    def code(self) -> str:
        return f"{self.tranche or ''}{self.system}{self.slot}JC-"

    @property
    def system_label(self) -> str | None:
        return describe_ecs_code(self.system)

    @property
    def support_kind(self) -> str:
        return "tableau" if self.slot[0] == "0" else "armoire"

    @property
    def enclosure_number(self) -> str | None:
        return None if self.support_kind == "tableau" else self.slot[0]

    @property
    def column(self) -> str:
        return self.slot[1]

    @property
    def row(self) -> str:
        return self.slot[2]

    @property
    def subcolumn(self) -> str:
        return self.slot[3]

    def __str__(self) -> str:
        return self.code


def parse_location_reference(value: str) -> LocationReference:
    """Parse an ECS localisation characteristic."""

    normalized = normalize_characteristic(value)
    match = LOCATION_PATTERN.fullmatch(normalized)
    if not match:
        msg = f"Invalid ECS location reference: {value!r}"
        raise ValueError(msg)
    groups = match.groupdict()
    return LocationReference(
        tranche=groups["tranche"],
        building=parse_building_trigram(groups["building"]).code,
        identification=BuildingIdentification(groups["identification"]),
        local_kind=groups["kind"],
    )


def parse_fire_sector_reference(value: str) -> FireSectorReference:
    """Parse an ECS fire sectorisation characteristic."""

    normalized = normalize_characteristic(value)
    match = FIRE_PATTERN.fullmatch(normalized)
    if not match:
        msg = f"Invalid ECS fire sector reference: {value!r}"
        raise ValueError(msg)
    groups = match.groupdict()
    if groups["kind"] == "Z" and groups["criterion"] == "C":
        msg = f"Invalid ECS fire sector reference: {value!r}"
        raise ValueError(msg)
    return FireSectorReference(
        tranche=groups["tranche"],
        building=parse_building_trigram(groups["building"]).code,
        identification=BuildingIdentification(groups["identification"]),
        kind=groups["kind"],
        criterion=groups["criterion"],
    )


def parse_electrical_supply_reference(value: str) -> ElectricalSupplyReference:
    """Parse an ECS electrical supply characteristic."""

    normalized = normalize_characteristic(value)
    match = ELECTRICAL_SUPPLY_PATTERN.fullmatch(normalized)
    if not match:
        msg = f"Invalid ECS electrical supply reference: {value!r}"
        raise ValueError(msg)
    groups = match.groupdict()
    return ElectricalSupplyReference(
        tranche=groups["tranche"],
        system=normalize_ecs_code(groups["system"]),
        slot=groups["slot"],
    )


def build_location_regex(*, tranche: str | None = None, building: str | None = None, local_kind: str | None = None) -> re.Pattern[str]:
    """Build a regex for localisation characteristics."""

    pattern = (
        (re.escape(str(tranche)) if tranche is not None else r"[0-9]?")
        + (re.escape(normalize_characteristic(building)) if building is not None else r"H[A-Z]{2}")
        + r"[0-9]{4}"
        + "Z"
        + (re.escape(normalize_characteristic(local_kind)) if local_kind is not None else r"[ACLM]")
        + "-"
    )
    return re.compile(f"^{pattern}$")


def build_fire_sector_regex(
    *, tranche: str | None = None, building: str | None = None, kind: str | None = None, criterion: str | None = None
) -> re.Pattern[str]:
    """Build a regex for fire sectorisation characteristics."""

    pattern = (
        (re.escape(str(tranche)) if tranche is not None else r"[0-9]?")
        + (re.escape(normalize_characteristic(building)) if building is not None else r"H[A-Z]{2}")
        + r"[0-9]{4}"
        + (re.escape(normalize_characteristic(kind)) if kind is not None else r"[SZ]")
        + "F"
        + (re.escape(normalize_characteristic(criterion)) if criterion is not None else r"[CIS]")
    )
    return re.compile(f"^{pattern}$")


def build_electrical_supply_regex(
    *, tranche: str | None = None, system: str | None = None
) -> re.Pattern[str]:
    """Build a regex for electrical supply characteristics."""

    pattern = (
        (re.escape(str(tranche)) if tranche is not None else r"[0-9]?")
        + (re.escape(normalize_ecs_code(system)) if system is not None else r"L[A-Z]{2}")
        + r"[0-9][A-Z0-9][A-Z0-9][0-9]JC-"
    )
    return re.compile(f"^{pattern}$")


def find_location_references(text: str) -> list[LocationReference]:
    """Find every localisation characteristic in a text."""

    return [parse_location_reference(match.group("value")) for match in LOCATION_FINDER_PATTERN.finditer(text.upper())]


def find_fire_sector_references(text: str) -> list[FireSectorReference]:
    """Find every fire sectorisation characteristic in a text."""

    return [parse_fire_sector_reference(match.group("value")) for match in FIRE_FINDER_PATTERN.finditer(text.upper())]


def find_electrical_supply_references(text: str) -> list[ElectricalSupplyReference]:
    """Find every electrical supply characteristic in a text."""

    return [
        parse_electrical_supply_reference(match.group("value"))
        for match in ELECTRICAL_SUPPLY_FINDER_PATTERN.finditer(text.upper())
    ]
