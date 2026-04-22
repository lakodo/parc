"""Helpers to parse and manipulate ECS repères fonctionnels (RF)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .ecs import KNOWN_ECS_CODES, describe_ecs_code, normalize_ecs_code
from .matching import proposal_can_match_completion, proposal_matches_candidate
from .materials import MATERIAL_CODE_LABELS, MaterialCodeDescription, describe_extension, describe_material_code

RF_REGEX = (
    r"(?P<tranche>[0-9])?"
    r"(?P<system>[A-Z]{3})"
    r"(?P<identification>[0-9]{3,4})"
    r"(?P<material_bigram>[A-Z]{2})"
    r"(?P<material_qualifier>[A-Z0-9-])"
    r"(?P<extension>[A-Z0-9]{0,4})"
)
RF_PATTERN = re.compile(f"^{RF_REGEX}$")
RF_FINDER_PATTERN = re.compile(rf"(?<![A-Z0-9])(?P<rf>{RF_REGEX})(?![A-Z0-9])")
RF_QUALIFIER_CHARS = ("-", *tuple("0123456789"), *tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
RF_EXTENSION_CHARS = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
RF_QUALIFIER_PASSES = (("-",), tuple(char for char in RF_QUALIFIER_CHARS if char != "-"))
KNOWN_RF_SYSTEM_CODES = tuple(sorted(code for code in KNOWN_ECS_CODES if len(code) == 3 and code.isalpha()))
KNOWN_RF_MATERIAL_BIGRAMS = tuple(sorted(MATERIAL_CODE_LABELS))


@dataclass(frozen=True)
class IdentificationSection:
    """Section 2 of an RF."""

    raw: str

    @property
    def is_compact(self) -> bool:
        return len(self.raw) == 3

    @property
    def sub_function(self) -> int | None:
        if self.is_compact:
            return None
        return int(self.raw[0])

    @property
    def base_function(self) -> int:
        if self.is_compact:
            return int(self.raw[0])
        return int(self.raw[1])

    @property
    def order(self) -> int:
        if self.is_compact:
            return int(self.raw[1:])
        return int(self.raw[2:])


@dataclass(frozen=True)
class MaterialSection:
    """Section 3 of an RF."""

    bigram: str
    qualifier: str

    @property
    def code(self) -> str:
        return f"{self.bigram}{self.qualifier}"

    @property
    def description(self) -> MaterialCodeDescription:
        return describe_material_code(self.code)

    @property
    def labels(self) -> tuple[str, ...]:
        return self.description.labels

    @property
    def qualifier_meanings(self) -> tuple[str, ...]:
        return self.description.qualifier_meanings


@dataclass(frozen=True)
class FunctionalReference:
    """Parsed ECS repère fonctionnel."""

    tranche: str | None
    system: str
    identification: IdentificationSection
    material: MaterialSection
    extension: str = ""

    @property
    def system_label(self) -> str | None:
        return describe_ecs_code(self.system)

    @property
    def canonical(self) -> str:
        return (
            f"{self.tranche or ''}"
            f"{self.system}"
            f"{self.identification.raw}"
            f"{self.material.code}"
            f"{self.extension}"
        )

    @property
    def extension_meanings(self) -> tuple[str, ...]:
        return describe_extension(self.material.code, self.extension)

    def with_extension(self, extension: str) -> FunctionalReference:
        return FunctionalReference(
            tranche=self.tranche,
            system=self.system,
            identification=self.identification,
            material=self.material,
            extension=normalize_rf_token(extension),
        )

    def __str__(self) -> str:
        return self.canonical


@dataclass(frozen=True)
class RFValidationResult:
    """Result of an RF validation or completion attempt."""

    query: str
    normalized_query: str
    is_exact_match: bool
    candidates: tuple[FunctionalReference, ...]
    truncated: bool = False

    @property
    def uses_pattern(self) -> bool:
        return "*" in self.normalized_query or "?" in self.normalized_query

    @property
    def has_candidates(self) -> bool:
        return bool(self.candidates)


def normalize_rf_token(value: str) -> str:
    """Normalize a single RF token."""

    return value.strip().upper().replace(" ", "")


def normalize_rf(value: str) -> str:
    """Normalize a full RF while preserving ECS semantics."""

    return normalize_rf_token(value)


def normalize_rf_query(value: str) -> str:
    """Normalize an RF validation query while preserving ``*`` and ``?``."""

    return normalize_rf_token(value)


def parse_rf(value: str) -> FunctionalReference:
    """Parse an ECS repère fonctionnel."""

    normalized = normalize_rf(value)
    match = RF_PATTERN.fullmatch(normalized)
    if not match:
        msg = f"Invalid ECS RF: {value!r}"
        raise ValueError(msg)

    groups = match.groupdict()
    system = normalize_ecs_code(groups["system"])
    if describe_ecs_code(system) is None:
        msg = f"Invalid ECS RF: {value!r}"
        raise ValueError(msg)
    return FunctionalReference(
        tranche=groups["tranche"],
        system=system,
        identification=IdentificationSection(groups["identification"]),
        material=MaterialSection(groups["material_bigram"], groups["material_qualifier"]),
        extension=groups["extension"],
    )


def is_rf(value: str) -> bool:
    """Return ``True`` if ``value`` is a valid ECS RF."""

    try:
        parse_rf(value)
    except ValueError:
        return False
    return True


def _identification_candidates() -> tuple[str, ...]:
    compact = tuple(f"{value:03d}" for value in range(1000))
    full = tuple(f"{value:04d}" for value in range(10000))
    return compact + full


IDENTIFICATION_CANDIDATES = _identification_candidates()


def _iter_extension_candidates(prefix: str, query: str, max_length: int = 4):
    if max_length == 0 or not proposal_can_match_completion(query, prefix):
        return

    for char in RF_EXTENSION_CHARS:
        next_prefix = prefix + char
        if not proposal_can_match_completion(query, next_prefix):
            continue
        if proposal_matches_candidate(query, next_prefix):
            yield next_prefix
        yield from _iter_extension_candidates(next_prefix, query, max_length=max_length - 1)


def _iter_tranche_prefixes(query: str):
    for tranche in ("", *tuple("0123456789")):
        if tranche and not proposal_can_match_completion(query, tranche):
            continue
        yield tranche


def _iter_system_prefixes(query: str, tranche_prefix: str):
    for system in KNOWN_RF_SYSTEM_CODES:
        prefix = f"{tranche_prefix}{system}"
        if not proposal_can_match_completion(query, prefix):
            continue
        yield prefix


def _iter_identification_prefixes(query: str, system_prefix: str):
    for identification in IDENTIFICATION_CANDIDATES:
        prefix = f"{system_prefix}{identification}"
        if not proposal_can_match_completion(query, prefix):
            continue
        yield prefix


def _iter_material_prefixes(query: str, identification_prefix: str):
    for material_bigram in KNOWN_RF_MATERIAL_BIGRAMS:
        prefix = f"{identification_prefix}{material_bigram}"
        if not proposal_can_match_completion(query, prefix):
            continue
        yield prefix


def _iter_base_candidates(query: str):
    for qualifier_choices in RF_QUALIFIER_PASSES:
        for tranche_prefix in _iter_tranche_prefixes(query):
            for system_prefix in _iter_system_prefixes(query, tranche_prefix):
                for identification_prefix in _iter_identification_prefixes(query, system_prefix):
                    for material_prefix in _iter_material_prefixes(query, identification_prefix):
                        for qualifier in qualifier_choices:
                            candidate = f"{material_prefix}{qualifier}"
                            if not proposal_can_match_completion(query, candidate):
                                continue
                            yield candidate


def suggest_rf_candidates(query: str, *, limit: int = 20) -> tuple[FunctionalReference, ...]:
    """Return candidate RF completions for a query or minimatch-like proposal."""

    normalized_query = normalize_rf_query(query)
    if not normalized_query:
        return ()

    candidates: list[FunctionalReference] = []
    seen: set[str] = set()

    def add(candidate: str) -> bool:
        if candidate in seen or not proposal_matches_candidate(normalized_query, candidate):
            return False
        try:
            parsed = parse_rf(candidate)
        except ValueError:
            return False
        seen.add(candidate)
        candidates.append(parsed)
        return len(candidates) >= limit

    base_candidates: list[str] = []
    for base_candidate in _iter_base_candidates(normalized_query):
        base_candidates.append(base_candidate)
        if add(base_candidate):
            return tuple(candidates)

    for base_candidate in base_candidates:
        for candidate in _iter_extension_candidates(base_candidate, normalized_query):
            if add(candidate):
                return tuple(candidates)

    return tuple(candidates)


def validate_rf(query: str, *, limit: int = 20) -> RFValidationResult:
    """Validate or complete an RF proposal.

    The query may be:
    - an exact RF
    - a partial RF prefix
    - a minimatch-like pattern using ``?`` and ``*``
    """

    normalized_query = normalize_rf_query(query)
    try:
        exact = parse_rf(normalized_query)
    except ValueError:
        exact = None

    if exact is not None:
        return RFValidationResult(
            query=query,
            normalized_query=normalized_query,
            is_exact_match=True,
            candidates=(exact,),
            truncated=False,
        )

    candidates = suggest_rf_candidates(normalized_query, limit=limit + 1)
    truncated = len(candidates) > limit
    if truncated:
        candidates = candidates[:limit]

    return RFValidationResult(
        query=query,
        normalized_query=normalized_query,
        is_exact_match=False,
        candidates=candidates,
        truncated=truncated,
    )


def build_rf(
    *,
    tranche: str | int | None,
    system: str,
    identification: str | int,
    material: str,
    extension: str = "",
) -> FunctionalReference:
    """Build an RF from explicit sections."""

    tranche_str = "" if tranche is None else str(tranche)
    identification_str = f"{int(identification):04d}" if isinstance(identification, int) else str(identification)
    material_code = normalize_rf_token(material)
    if len(material_code) == 2:
        material_code = f"{material_code}-"
    return parse_rf(f"{tranche_str}{normalize_ecs_code(system)}{identification_str}{material_code}{extension}")


def build_rf_regex(
    *,
    tranche: str | None = None,
    system: str | None = None,
    identification: str | None = None,
    material: str | None = None,
    extension: str | None = None,
    anchored: bool = True,
) -> re.Pattern[str]:
    """Build a regex for RF matching from exact section values."""

    material = normalize_rf_token(material) if material else None
    if material and len(material) == 2:
        material = f"{material}-"

    pattern = (
        (re.escape(str(tranche)) if tranche is not None else r"[0-9]?")
        + (re.escape(normalize_ecs_code(system)) if system is not None else r"[A-Z]{3}")
        + (re.escape(str(identification)) if identification is not None else r"[0-9]{3,4}")
        + (re.escape(material[:2]) if material is not None else r"[A-Z]{2}")
        + (re.escape(material[2]) if material is not None else r"[A-Z0-9-]")
        + (re.escape(normalize_rf_token(extension)) if extension is not None else r"[A-Z0-9]{0,4}")
    )
    if anchored:
        pattern = f"^{pattern}$"
    return re.compile(pattern)


def find_rfs(text: str) -> list[FunctionalReference]:
    """Extract every canonical RF found in a block of text."""

    found: list[FunctionalReference] = []
    for match in RF_FINDER_PATTERN.finditer(text.upper()):
        found.append(parse_rf(match.group("rf")))
    return found
