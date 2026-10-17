"""Text preprocessing: normalisation, tokenisation and stemming."""

import re

from nltk.stem import PorterStemmer

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
_stemmer = PorterStemmer()

# Politeness filler that carries no intent signal. Question words ("what",
# "how") are deliberately kept because they separate intents like time/date.
FILLER_WORDS = frozenset(
    {"a", "an", "the", "please", "pls", "plz", "kindly", "could", "would",
     "can", "you", "u", "me", "for", "hey", "ok", "okay", "just"}
)


def normalize(text: str) -> str:
    """Lowercase, unify apostrophes and drop invisible byte-order marks."""
    return text.replace("﻿", "").lower().replace("’", "'").strip()


def tokenize(text: str) -> list[str]:
    """Split normalised text into word tokens, keeping contractions together."""
    return _TOKEN_RE.findall(normalize(text))


def stem(tokens: list[str]) -> list[str]:
    """Reduce each token to its Porter stem (``opening`` -> ``open``)."""
    return [_stemmer.stem(token) for token in tokens]


def preprocess(text: str) -> str:
    """Full pipeline used by the vectorizer: tokenize, drop filler, stem."""
    tokens = [t for t in tokenize(text) if t not in FILLER_WORDS]
    if not tokens:  # e.g. "hey" on its own: keep it rather than return nothing
        tokens = tokenize(text)
    return " ".join(stem(tokens))
