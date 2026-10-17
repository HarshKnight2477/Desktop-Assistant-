"""Load and validate the intents dataset."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from assistant import config


@dataclass(frozen=True)
class Intent:
    tag: str
    patterns: list[str]
    responses: list[str]
    action: str | None = None
    ends_conversation: bool = False


@dataclass(frozen=True)
class IntentDataset:
    intents: dict[str, Intent]
    fallback: list[str] = field(default_factory=list)

    def training_data(self) -> tuple[list[str], list[str]]:
        texts, labels = [], []
        for intent in self.intents.values():
            texts.extend(intent.patterns)
            labels.extend([intent.tag] * len(intent.patterns))
        return texts, labels


def load_intents(path: Path = config.INTENTS_PATH) -> IntentDataset:
    raw = json.loads(path.read_text(encoding="utf-8"))
    intents: dict[str, Intent] = {}
    for item in raw["intents"]:
        intent = Intent(
            tag=item["tag"],
            patterns=item["patterns"],
            responses=item["responses"],
            action=item.get("action"),
            ends_conversation=item.get("ends_conversation", False),
        )
        if intent.tag in intents:
            raise ValueError(f"Duplicate intent tag: {intent.tag}")
        if not intent.patterns or not intent.responses:
            raise ValueError(f"Intent {intent.tag!r} needs patterns and responses")
        intents[intent.tag] = intent
    return IntentDataset(intents=intents, fallback=raw.get("fallback", []))


def load_test_phrases(path: Path = config.TEST_PHRASES_PATH) -> list[tuple[str, str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [(text, tag) for text, tag in raw["phrases"]]
