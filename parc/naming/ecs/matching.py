"""Wildcard helpers shared by ECS validators."""

from __future__ import annotations

from functools import cache

GLOB_STAR = "*"
GLOB_SINGLE = "?"


def proposal_matches_candidate(query: str, candidate: str) -> bool:
    """Return ``True`` when a wildcard query matches a candidate value."""

    @cache
    def matches(query_index: int, candidate_index: int) -> bool:
        if query_index == len(query):
            return True
        if candidate_index == len(candidate):
            return all(char == GLOB_STAR for char in query[query_index:])

        query_token = query[query_index]
        if query_token == GLOB_STAR:
            return matches(query_index + 1, candidate_index) or matches(query_index, candidate_index + 1)
        if query_token == GLOB_SINGLE:
            return matches(query_index + 1, candidate_index + 1)
        if query_token == candidate[candidate_index]:
            return matches(query_index + 1, candidate_index + 1)
        return False

    return matches(0, 0)


def proposal_can_match_completion(query: str, prefix: str) -> bool:
    """Return ``True`` if a prefix can still be completed to satisfy ``query``."""

    @cache
    def matches(query_index: int, prefix_index: int) -> bool:
        if query_index == len(query) or prefix_index == len(prefix):
            return True

        query_token = query[query_index]
        if query_token == GLOB_STAR:
            return matches(query_index + 1, prefix_index) or matches(query_index, prefix_index + 1)
        if query_token == GLOB_SINGLE:
            return matches(query_index + 1, prefix_index + 1)
        if query_token == prefix[prefix_index]:
            return matches(query_index + 1, prefix_index + 1)
        return False

    return matches(0, 0)
