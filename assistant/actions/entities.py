"""Rule-based slot extraction (search query, city, app name, ...)."""

import re

from assistant.nlp.preprocessing import normalize

_SEARCH_PREFIX = re.compile(
    r"^(?:(?:can|could|would) you\s+)?(?:please\s+)?"
    r"(?:search|google|look\s+up|find(?:\s+me)?)"
    r"(?:\s+(?:the\s+web|online|the\s+internet))?"
    r"(?:\s+(?:for|about|on))?(?:\s+|$)"
)
_SEARCH_SUFFIX = re.compile(r"\s+(?:on\s+google|online|on\s+the\s+(?:web|internet))$")

_CITY = re.compile(r"\b(?:in|at|for|of)\s+([a-z][a-z .'-]*?)(?:\s+(?:today|now|tomorrow|please))?[?.!]*$")
_NOT_CITIES = {"today", "now", "outside", "here", "the day", "tomorrow"}

_DOMAIN = re.compile(r"\b([a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})\b")


def extract_search_query(text: str) -> str:
    query = _SEARCH_PREFIX.sub("", normalize(text), count=1)
    query = _SEARCH_SUFFIX.sub("", query)
    return query.strip(" ?.!")


def extract_city(text: str) -> str | None:
    match = _CITY.search(normalize(text))
    if not match:
        return None
    city = match.group(1).strip()
    return None if city in _NOT_CITIES else city.title()


def extract_domain(text: str) -> str | None:
    match = _DOMAIN.search(normalize(text))
    return match.group(1) if match else None


def find_keyword(text: str, keywords: dict[str, str]) -> str | None:
    """Return the value for the longest keyword phrase found in ``text``."""
    words = f" {' '.join(re.findall(r'[a-z0-9]+', normalize(text)))} "
    for keyword in sorted(keywords, key=len, reverse=True):
        if f" {keyword} " in words:
            return keywords[keyword]
    return None
