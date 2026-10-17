"""Response generation: pick a template for an intent and fill in its slots."""

import random
import string

from assistant import config
from assistant.data_loader import IntentDataset

DEFAULT_FALLBACK = "Sorry, I didn't understand that."


class ResponseEngine:
    def __init__(self, dataset: IntentDataset, rng: random.Random | None = None):
        self.dataset = dataset
        self.rng = rng or random.Random()
        self.base_slots = {"assistant_name": config.ASSISTANT_NAME}

    def respond(self, tag: str, slots: dict[str, str] | None = None) -> str:
        template = self.rng.choice(self.dataset.intents[tag].responses)
        return template.format_map(self.base_slots | (slots or {}))

    def fallback(self) -> str:
        return self.rng.choice(self.dataset.fallback or [DEFAULT_FALLBACK])


def template_fields(template: str) -> set[str]:
    """Names of the ``{placeholders}`` in a response template."""
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}
