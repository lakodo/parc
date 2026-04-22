"""Detection and reporting helpers for ECS references embedded in text."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .buildings import (
    STRUCTURE_CHARACTERISTIC_CODES,
    STRUCTURE_COMPONENT_CODES,
    STRUCTURE_ELEMENT_CODES,
    parse_building_trigram,
)
from .characteristics import (
    ELECTRICAL_SUPPLY_FINDER_PATTERN,
    FIRE_FINDER_PATTERN,
    LOCATION_FINDER_PATTERN,
    ElectricalSupplyReference,
    FireSectorReference,
    LocationReference,
    parse_electrical_supply_reference,
    parse_fire_sector_reference,
    parse_location_reference,
)
from .ecs import FUNCTIONAL_SET_CODES
from .geographic import RG_FINDER_PATTERN, GeographicReference, parse_rg
from .matching import proposal_can_match_completion, proposal_matches_candidate
from .rf import RF_FINDER_PATTERN, FunctionalReference, parse_rf, validate_rf

ParsedReference = (
    FunctionalReference | LocationReference | FireSectorReference | ElectricalSupplyReference | GeographicReference
)


@dataclass(frozen=True)
class ExtractedReference:
    """Reference-like token extracted from free text."""

    raw: str
    canonical: str
    start: int
    end: int
    kind: str | None = None


@dataclass(frozen=True)
class DetectedReference:
    """A parsed ECS reference detected inside a text."""

    kind: str
    raw: str
    start: int
    end: int
    parsed: ParsedReference

    @property
    def canonical(self) -> str:
        return str(self.parsed)


@dataclass(frozen=True)
class ReferenceValidationResult:
    """Result of a generic ECS reference validation or completion attempt."""

    query: str
    normalized_query: str
    is_exact_match: bool
    candidates: tuple[DetectedReference, ...]
    truncated: bool = False

    @property
    def has_candidates(self) -> bool:
        return bool(self.candidates)


DETECTOR_SPECS = (
    ("location", LOCATION_FINDER_PATTERN, "value", parse_location_reference),
    ("fire-sector", FIRE_FINDER_PATTERN, "value", parse_fire_sector_reference),
    ("electrical-supply", ELECTRICAL_SUPPLY_FINDER_PATTERN, "value", parse_electrical_supply_reference),
    ("rg", RG_FINDER_PATTERN, "value", parse_rg),
    ("rf", RF_FINDER_PATTERN, "rf", parse_rf),
)
REFERENCE_PARSERS = (
    ("location", parse_location_reference),
    ("fire-sector", parse_fire_sector_reference),
    ("electrical-supply", parse_electrical_supply_reference),
    ("rg", parse_rg),
    ("rf", parse_rf),
)

DIGITS = tuple("0123456789")
UPPER = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
ALNUM = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
RG_STRUCTURE_START = tuple("BCDEFJLMNPVX")
RG_STRUCTURE_END = tuple("-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LOCATION_CHARSETS = (
    DIGITS,
    ("H",),
    UPPER,
    UPPER,
    DIGITS,
    DIGITS,
    DIGITS,
    DIGITS,
    ("Z",),
    tuple("ACLM"),
    ("-",),
)
FIRE_CHARSETS = (
    DIGITS,
    ("H",),
    UPPER,
    UPPER,
    DIGITS,
    DIGITS,
    DIGITS,
    DIGITS,
    tuple("SZ"),
    ("F",),
    tuple("CIS"),
)
ELECTRICAL_SUPPLY_CHARSETS = (
    DIGITS,
    ("L",),
    UPPER,
    UPPER,
    DIGITS,
    ALNUM,
    ALNUM,
    DIGITS,
    ("J",),
    ("C",),
    ("-",),
)
RG_MANDATORY_CHARSETS = (
    DIGITS,
    ("H",),
    UPPER,
    UPPER,
    DIGITS,
    DIGITS,
    DIGITS,
    DIGITS,
    RG_STRUCTURE_START,
    UPPER,
    RG_STRUCTURE_END,
)
RG_OPTIONAL_CHARSETS = (ALNUM, ALNUM, ALNUM, ALNUM)
PATTERN_SPECS = (
    ("location", parse_location_reference, ("", *DIGITS), LOCATION_CHARSETS[1:], ()),
    ("fire-sector", parse_fire_sector_reference, ("", *DIGITS), FIRE_CHARSETS[1:], ()),
    ("electrical-supply", parse_electrical_supply_reference, ("", *DIGITS), ELECTRICAL_SUPPLY_CHARSETS[1:], ()),
    ("rg", parse_rg, ("", *DIGITS), RG_MANDATORY_CHARSETS[1:], RG_OPTIONAL_CHARSETS),
)


def normalize_reference_query(value: str) -> str:
    """Normalize a reference validation query while preserving wildcards."""

    return value.strip().upper().replace(" ", "")


def _build_detected_reference(kind: str, raw: str, parsed: ParsedReference) -> DetectedReference:
    return DetectedReference(
        kind=kind,
        raw=raw,
        start=0,
        end=len(raw),
        parsed=parsed,
    )


def _has_ecs_pattern_anchor(token: str) -> bool:
    """Return ``True`` when a wildcard token starts like an ECS reference.

    We intentionally require an early trigram anchor before preserving a ``*``
    pattern as extractable text. This keeps broad patterns such as ``0*PO``
    from being treated as meaningful ECS references while still accepting
    patterns like ``RCV*`` or ``1HRA*``.
    """

    prefix = token.split("*", 1)[0].split("?", 1)[0]
    if not prefix:
        return False

    if len(prefix) >= 3 and prefix[:3].isalpha():
        return True
    return len(prefix) >= 4 and prefix[0].isdigit() and prefix[1:4].isalpha()


def _iter_pattern_candidates(
    query: str,
    *,
    prefixes: tuple[str, ...],
    charsets: tuple[tuple[str, ...], ...],
    optional_charsets: tuple[tuple[str, ...], ...] = (),
):
    def walk(index: int, prefix: str):
        if not proposal_can_match_completion(query, prefix):
            return
        if index == len(charsets):
            yield prefix
            yield from walk_optional(0, prefix)
            return
        for char in charsets[index]:
            yield from walk(index + 1, prefix + char)

    def walk_optional(index: int, prefix: str):
        if not proposal_can_match_completion(query, prefix):
            return
        if index == len(optional_charsets):
            return
        for char in optional_charsets[index]:
            next_prefix = prefix + char
            yield next_prefix
            yield from walk_optional(index + 1, next_prefix)

    for prefix in prefixes:
        yield from walk(0, prefix)


def _pattern_candidates_for_kind(
    query: str,
    *,
    kind: str,
    parser,
    prefixes: tuple[str, ...],
    charsets: tuple[tuple[str, ...], ...],
    optional_charsets: tuple[tuple[str, ...], ...] = (),
):
    for candidate in _iter_pattern_candidates(
        query, prefixes=prefixes, charsets=charsets, optional_charsets=optional_charsets
    ):
        if not proposal_matches_candidate(query, candidate):
            continue
        try:
            parsed = parser(candidate)
        except ValueError:
            continue
        yield _build_detected_reference(kind, candidate, parsed)


def parse_reference(value: str) -> DetectedReference:
    """Parse a single ECS reference by trying every known exact type."""

    for kind, parser in REFERENCE_PARSERS:
        try:
            parsed = parser(value)
        except ValueError:
            continue
        return DetectedReference(
            kind=kind,
            raw=value,
            start=0,
            end=len(str(value)),
            parsed=parsed,
        )
    msg = f"Unknown ECS reference: {value!r}"
    raise ValueError(msg)


def validate_reference(query: str, *, limit: int = 20) -> ReferenceValidationResult:
    """Validate or complete a reference across all supported ECS types."""

    normalized_query = normalize_reference_query(query)
    try:
        exact = parse_reference(normalized_query)
    except ValueError:
        exact = None

    if exact is not None:
        return ReferenceValidationResult(
            query=query,
            normalized_query=normalized_query,
            is_exact_match=True,
            candidates=(exact,),
            truncated=False,
        )

    candidates: list[DetectedReference] = []
    seen: set[tuple[str, str]] = set()

    def add(detection: DetectedReference) -> bool:
        key = (detection.kind, detection.canonical)
        if key in seen:
            return False
        seen.add(key)
        candidates.append(detection)
        return len(candidates) > limit

    for kind, parser, prefixes, charsets, optional_charsets in PATTERN_SPECS:
        for detection in _pattern_candidates_for_kind(
            normalized_query,
            kind=kind,
            parser=parser,
            prefixes=prefixes,
            charsets=charsets,
            optional_charsets=optional_charsets,
        ):
            if add(detection):
                return ReferenceValidationResult(
                    query=query,
                    normalized_query=normalized_query,
                    is_exact_match=False,
                    candidates=tuple(candidates[:limit]),
                    truncated=True,
                )

    rf_result = validate_rf(normalized_query, limit=limit + 1)
    for candidate in rf_result.candidates:
        if add(_build_detected_reference("rf", str(candidate), candidate)):
            return ReferenceValidationResult(
                query=query,
                normalized_query=normalized_query,
                is_exact_match=False,
                candidates=tuple(candidates[:limit]),
                truncated=True,
            )

    return ReferenceValidationResult(
        query=query,
        normalized_query=normalized_query,
        is_exact_match=False,
        candidates=tuple(candidates[:limit]),
        truncated=len(candidates) > limit or rf_result.truncated,
    )


def analyze_text(text: str) -> list[DetectedReference]:
    """Detect ECS references inside arbitrary text."""

    detections: list[DetectedReference] = []
    seen: set[tuple[int, int]] = set()

    for kind, pattern, group_name, parser in DETECTOR_SPECS:
        for match in pattern.finditer(text.upper()):
            start, end = match.span(group_name)
            key = (start, end)
            if key in seen:
                continue
            try:
                parsed = parser(match.group(group_name))
            except ValueError:
                continue
            seen.add(key)
            raw = text[start:end]
            detections.append(
                DetectedReference(
                    kind=kind,
                    raw=raw,
                    start=start,
                    end=end,
                    parsed=parsed,
                )
            )

    return sorted(detections, key=lambda item: (item.start, item.end, item.kind))


EXTRACT_TOKEN_PATTERN = re.compile(r"(?P<token>[A-Z0-9?*-]{4,})")


def extract_references(text: str) -> list[ExtractedReference]:
    """Extract canonical ECS references from free text.

    This extractor is intentionally conservative: it accepts exact references,
    plus obvious normalizations such as a missing trailing ``-`` when the
    completed form becomes an exact ECS reference.
    """

    detections: list[ExtractedReference] = []

    for match in EXTRACT_TOKEN_PATTERN.finditer(text.upper()):
        raw = text[match.start("token") : match.end("token")]
        token = raw.strip().upper()

        detection: DetectedReference | None = None
        try:
            detection = parse_reference(token)
        except ValueError:
            if not token.endswith("-"):
                try:
                    detection = parse_reference(f"{token}-")
                except ValueError:
                    detection = None

        if detection is None and "*" in token and _has_ecs_pattern_anchor(token):
            detections.append(
                ExtractedReference(
                    raw=raw,
                    canonical=token,
                    start=match.start("token"),
                    end=match.end("token"),
                    kind="pattern",
                )
            )
            continue

        if detection is None and "?" in token:
            result = validate_reference(token, limit=2)
            if len(result.candidates) == 1:
                detection = result.candidates[0]
            elif result.candidates:
                detections.append(
                    ExtractedReference(
                        raw=raw,
                        canonical=token,
                        start=match.start("token"),
                        end=match.end("token"),
                        kind="pattern",
                    )
                )
                continue

        if detection is None:
            continue

        detections.append(
            ExtractedReference(
                raw=raw,
                canonical=detection.canonical,
                start=match.start("token"),
                end=match.end("token"),
                kind=detection.kind,
            )
        )

    return detections


def _format_altitude_range(altitude_range: tuple[float, float] | None) -> str | None:
    if altitude_range is None:
        return None
    return f"{altitude_range[0]:+.2f} -> {altitude_range[1]:+.2f}"


def _append(lines: list[str], label: str, value: object) -> None:
    if value in (None, "", (), []):
        return
    if isinstance(value, tuple):
        value = ", ".join(str(item) for item in value)
    lines.append(f"{label}: {value}")


def _append_detail(lines: list[str], label: str, value: object, meaning: object | None = None) -> None:
    if isinstance(value, tuple):
        value = ", ".join(str(item) for item in value)
    if isinstance(meaning, tuple):
        meaning = ", ".join(str(item) for item in meaning)
    if value in (None, "", (), []):
        return
    if meaning in (None, "", (), []):
        lines.append(f"{label}: {value}")
        return
    lines.append(f"{label}: {value} -> {meaning}")


def _format_meanings(meanings: tuple[str, ...], *, fallback: str | None = None) -> str | None:
    if meanings:
        return ", ".join(meanings)
    return fallback


def _append_building_breakdown(lines: list[str], building: str) -> None:
    trigram = parse_building_trigram(building)
    _append_detail(lines, "    building_segment", trigram.code, trigram.family_label)
    _append_detail(lines, "    building_char_1", trigram.code[0], "Préfixe des bâtiments et ouvrages")
    _append_detail(lines, "    building_char_2", trigram.family, trigram.family_label)
    _append_detail(lines, "    building_char_3", trigram.zone, "Zone ou sous-ensemble interne du bâtiment")


def _append_system_breakdown(lines: list[str], system: str, system_label: str | None) -> None:
    _append_detail(lines, "    system_segment", system, system_label)
    _append_detail(lines, "    system_letter_1", system[0], FUNCTIONAL_SET_CODES.get(system[0]))
    if len(system) > 1:
        _append_detail(
            lines,
            "    system_letters_2_3",
            system[1:],
            "Partie spécifique du trigramme système",
        )


def _append_rf_breakdown(lines: list[str], parsed: FunctionalReference) -> None:
    lines.append("  decomposition:")
    _append_detail(
        lines,
        "    tranche_segment",
        parsed.tranche or "<absent>",
        "Tranche non précisée" if parsed.tranche is None else f"Tranche {parsed.tranche}",
    )
    _append_system_breakdown(lines, parsed.system, parsed.system_label)
    if parsed.identification.is_compact:
        _append_detail(
            lines,
            "    identification_segment",
            parsed.identification.raw,
            "Format compact sans sous-fonction",
        )
        _append_detail(lines, "    identification_digit_1", parsed.identification.raw[0], "Fonction de base")
        _append_detail(
            lines,
            "    identification_digits_2_3",
            parsed.identification.raw[1:],
            f"Ordre {parsed.identification.order}",
        )
    else:
        _append_detail(lines, "    identification_segment", parsed.identification.raw, "Format complet")
        _append_detail(
            lines,
            "    identification_digit_1",
            parsed.identification.raw[0],
            f"Sous-fonction {parsed.identification.sub_function}",
        )
        _append_detail(
            lines,
            "    identification_digit_2",
            parsed.identification.raw[1],
            f"Fonction de base {parsed.identification.base_function}",
        )
        _append_detail(
            lines,
            "    identification_digits_3_4",
            parsed.identification.raw[2:],
            f"Ordre {parsed.identification.order}",
        )
    _append_detail(lines, "    material_segment", parsed.material.code)
    _append_detail(lines, "    material_bigram", parsed.material.bigram, parsed.material.labels)
    _append_detail(
        lines,
        "    material_qualifier",
        parsed.material.qualifier,
        _format_meanings(parsed.material.qualifier_meanings, fallback="Qualificatif absent ou non précisé"),
    )
    if parsed.extension:
        _append_detail(
            lines,
            "    extension_segment",
            parsed.extension,
            _format_meanings(parsed.extension_meanings, fallback="Extension sans interprétation connue"),
        )


def _append_location_breakdown(lines: list[str], parsed: LocationReference) -> None:
    lines.append("  decomposition:")
    _append_detail(
        lines,
        "    tranche_segment",
        parsed.tranche or "<absent>",
        "Tranche non précisée" if parsed.tranche is None else f"Tranche {parsed.tranche}",
    )
    _append_building_breakdown(lines, parsed.building)
    _append_detail(lines, "    identification_segment", parsed.identification.raw)
    _append_detail(lines, "    level_digits", parsed.identification.level, f"Niveau {parsed.identification.level}")
    _append_detail(
        lines,
        "    level_altitude_range",
        _format_altitude_range(parsed.identification.altitude_range),
    )
    _append_detail(lines, "    local_digits", parsed.identification.sequence, f"Repère local {parsed.local_number}")
    _append_detail(lines, "    suffix_segment", f"Z{parsed.local_kind}-", parsed.local_kind_label)
    _append_detail(lines, "    suffix_char_1", "Z", "Marqueur de caractéristique de localisation")
    _append_detail(lines, "    suffix_char_2", parsed.local_kind, parsed.local_kind_label)
    _append_detail(lines, "    suffix_char_3", "-", "Séparateur fixe")


def _append_fire_breakdown(lines: list[str], parsed: FireSectorReference) -> None:
    lines.append("  decomposition:")
    _append_detail(
        lines,
        "    tranche_segment",
        parsed.tranche or "<absent>",
        "Tranche non précisée" if parsed.tranche is None else f"Tranche {parsed.tranche}",
    )
    _append_building_breakdown(lines, parsed.building)
    _append_detail(lines, "    identification_segment", parsed.identification.raw)
    _append_detail(lines, "    level_digits", parsed.identification.level, f"Niveau {parsed.identification.level}")
    _append_detail(
        lines,
        "    level_altitude_range",
        _format_altitude_range(parsed.identification.altitude_range),
    )
    _append_detail(lines, "    sector_digits", parsed.identification.sequence, f"Repère secteur {parsed.sector_number}")
    _append_detail(
        lines,
        "    suffix_segment",
        f"{parsed.kind}F{parsed.criterion}",
        f"{parsed.kind_label}, critère {parsed.criterion_label}",
    )
    _append_detail(lines, "    suffix_char_1", parsed.kind, parsed.kind_label)
    _append_detail(lines, "    suffix_char_2", "F", "Marqueur incendie / feu")
    _append_detail(lines, "    suffix_char_3", parsed.criterion, parsed.criterion_label)


def _append_electrical_supply_breakdown(lines: list[str], parsed: ElectricalSupplyReference) -> None:
    lines.append("  decomposition:")
    _append_detail(
        lines,
        "    tranche_segment",
        parsed.tranche or "<absent>",
        "Tranche non précisée" if parsed.tranche is None else f"Tranche {parsed.tranche}",
    )
    _append_system_breakdown(lines, parsed.system, parsed.system_label)
    _append_detail(lines, "    slot_segment", parsed.slot, parsed.support_kind)
    _append_detail(lines, "    slot_char_1", parsed.slot[0], parsed.support_kind)
    _append_detail(lines, "    slot_char_2", parsed.slot[1], f"Colonne {parsed.column}")
    _append_detail(lines, "    slot_char_3", parsed.slot[2], f"Rangée {parsed.row}")
    _append_detail(lines, "    slot_char_4", parsed.slot[3], f"Sous-colonne {parsed.subcolumn}")
    _append_detail(lines, "    suffix_segment", "JC-", "Cellule électrique")
    _append_detail(lines, "    suffix_bigram", "JC", "Cellule électrique")
    _append_detail(lines, "    suffix_char_3", "-", "Séparateur fixe")


def _append_rg_breakdown(lines: list[str], parsed: GeographicReference) -> None:
    lines.append("  decomposition:")
    _append_detail(
        lines,
        "    tranche_segment",
        parsed.tranche or "<absent>",
        "Tranche non précisée" if parsed.tranche is None else f"Tranche {parsed.tranche}",
    )
    _append_building_breakdown(lines, parsed.building)
    _append_detail(lines, "    identification_segment", parsed.identification.raw)
    _append_detail(lines, "    level_digits", parsed.identification.level, f"Niveau {parsed.identification.level}")
    _append_detail(
        lines,
        "    level_altitude_range",
        _format_altitude_range(parsed.identification.altitude_range),
    )
    _append_detail(lines, "    order_digits", parsed.identification.order, f"Ordre {parsed.identification.order}")
    _append_detail(lines, "    structure_segment", parsed.structure, parsed.structure_meanings)
    if parsed.structure[0] == "C":
        _append_detail(
            lines, "    structure_char_1", parsed.structure[0], STRUCTURE_ELEMENT_CODES.get(parsed.structure[0])
        )
        _append_detail(lines, "    structure_char_2", parsed.structure[1], f"Voie électrique {parsed.structure[1]}")
        _append_detail(lines, "    structure_char_3", parsed.structure[2], f"Tablette {parsed.structure[2]}")
    else:
        _append_detail(
            lines, "    structure_char_1", parsed.structure[0], STRUCTURE_ELEMENT_CODES.get(parsed.structure[0])
        )
        _append_detail(
            lines, "    structure_char_2", parsed.structure[1], STRUCTURE_CHARACTERISTIC_CODES.get(parsed.structure[1])
        )
        if parsed.structure[2] == "-":
            _append_detail(lines, "    structure_char_3", parsed.structure[2], "Pas de composant précisé")
        else:
            _append_detail(
                lines, "    structure_char_3", parsed.structure[2], STRUCTURE_COMPONENT_CODES.get(parsed.structure[2])
            )
    if parsed.extension:
        _append_detail(
            lines,
            "    extension_segment",
            parsed.extension,
            _format_meanings(parsed.extension_meanings, fallback="Extension sans interprétation connue"),
        )


def format_detection(detection: DetectedReference) -> str:
    """Render one detection as a human-readable block."""

    parsed = detection.parsed
    lines = [
        f"- type: {detection.kind}",
        f"  raw: {detection.raw}",
        f"  canonical: {detection.canonical}",
        f"  span: {detection.start}-{detection.end}",
    ]

    if isinstance(parsed, FunctionalReference):
        _append(lines, "  tranche", parsed.tranche)
        _append(lines, "  system", parsed.system)
        _append(lines, "  system_label", parsed.system_label)
        _append(lines, "  identification", parsed.identification.raw)
        _append(lines, "  sub_function", parsed.identification.sub_function)
        _append(lines, "  base_function", parsed.identification.base_function)
        _append(lines, "  order", parsed.identification.order)
        _append(lines, "  material", parsed.material.code)
        _append(lines, "  material_labels", parsed.material.labels)
        _append(lines, "  material_qualifier_meanings", parsed.material.qualifier_meanings)
        _append(lines, "  extension", parsed.extension)
        _append(lines, "  extension_meanings", parsed.extension_meanings)
        _append_rf_breakdown(lines, parsed)
        return "\n".join(lines)

    if isinstance(parsed, LocationReference):
        _append(lines, "  tranche", parsed.tranche)
        _append(lines, "  building", parsed.building)
        _append(lines, "  building_label", parsed.building_label)
        _append(lines, "  level", parsed.identification.level)
        _append(lines, "  altitude_range", _format_altitude_range(parsed.identification.altitude_range))
        _append(lines, "  local_number", parsed.local_number)
        _append(lines, "  local_kind", parsed.local_kind)
        _append(lines, "  local_kind_label", parsed.local_kind_label)
        _append_location_breakdown(lines, parsed)
        return "\n".join(lines)

    if isinstance(parsed, FireSectorReference):
        _append(lines, "  tranche", parsed.tranche)
        _append(lines, "  building", parsed.building)
        _append(lines, "  building_label", parsed.building_label)
        _append(lines, "  level", parsed.identification.level)
        _append(lines, "  altitude_range", _format_altitude_range(parsed.identification.altitude_range))
        _append(lines, "  sector_number", parsed.sector_number)
        _append(lines, "  fire_kind", parsed.kind)
        _append(lines, "  fire_kind_label", parsed.kind_label)
        _append(lines, "  criterion", parsed.criterion)
        _append(lines, "  criterion_label", parsed.criterion_label)
        _append(lines, "  fire_order_rank", parsed.rank)
        _append_fire_breakdown(lines, parsed)
        return "\n".join(lines)

    if isinstance(parsed, ElectricalSupplyReference):
        _append(lines, "  tranche", parsed.tranche)
        _append(lines, "  system", parsed.system)
        _append(lines, "  system_label", parsed.system_label)
        _append(lines, "  slot", parsed.slot)
        _append(lines, "  support_kind", parsed.support_kind)
        _append(lines, "  enclosure_number", parsed.enclosure_number)
        _append(lines, "  column", parsed.column)
        _append(lines, "  row", parsed.row)
        _append(lines, "  subcolumn", parsed.subcolumn)
        _append_electrical_supply_breakdown(lines, parsed)
        return "\n".join(lines)

    if isinstance(parsed, GeographicReference):
        _append(lines, "  tranche", parsed.tranche)
        _append(lines, "  building", parsed.building)
        _append(lines, "  building_label", parsed.building_label)
        _append(lines, "  level", parsed.identification.level)
        _append(lines, "  altitude_range", _format_altitude_range(parsed.identification.altitude_range))
        _append(lines, "  order", parsed.identification.order)
        _append(lines, "  structure", parsed.structure)
        _append(lines, "  structure_meanings", parsed.structure_meanings)
        _append(lines, "  extension", parsed.extension)
        _append(lines, "  extension_meanings", parsed.extension_meanings)
        _append_rg_breakdown(lines, parsed)
        return "\n".join(lines)

    return "\n".join(lines)


def format_report(detections: list[DetectedReference]) -> str:
    """Render a full report for multiple detections."""

    if not detections:
        return "No ECS reference detected."
    blocks = [format_detection(detection) for detection in detections]
    return "\n\n".join(blocks)
