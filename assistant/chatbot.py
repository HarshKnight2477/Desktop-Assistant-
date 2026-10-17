"""The chatbot: classify the message, run the intent's action, build the reply."""

import time
from dataclasses import dataclass

from assistant import config
from assistant.actions import DEFAULT_ACTIONS, Action, ActionError
from assistant.data_loader import IntentDataset, load_intents
from assistant.nlp import IntentClassifier
from assistant.responses import ResponseEngine

FALLBACK_INTENT = "fallback"


@dataclass(frozen=True)
class Reply:
    text: str
    intent: str
    confidence: float
    latency_ms: float
    ends_conversation: bool = False


class Chatbot:
    def __init__(
        self,
        classifier: IntentClassifier,
        dataset: IntentDataset,
        actions: dict[str, Action] | None = None,
        threshold: float = config.CONFIDENCE_THRESHOLD,
        responses: ResponseEngine | None = None,
    ):
        self.classifier = classifier
        self.dataset = dataset
        self.actions = DEFAULT_ACTIONS if actions is None else actions
        self.threshold = threshold
        self.responses = responses or ResponseEngine(dataset)

    @classmethod
    def from_disk(cls) -> "Chatbot":
        """Load the trained model, training it first if it doesn't exist yet."""
        dataset = load_intents()
        if config.MODEL_PATH.exists():
            classifier = IntentClassifier.load(config.MODEL_PATH)
        else:
            from assistant.train import train
            classifier = train(dataset)
        return cls(classifier, dataset)

    def reply(self, message: str) -> Reply:
        start = time.perf_counter()
        text, intent, confidence, ends = self._respond(message)
        latency_ms = (time.perf_counter() - start) * 1000
        return Reply(text, intent, confidence, latency_ms, ends)

    def _respond(self, message: str) -> tuple[str, str, float, bool]:
        if not message.strip():
            return self.responses.fallback(), FALLBACK_INTENT, 0.0, False

        prediction = self.classifier.predict(message)
        if prediction.confidence < self.threshold:
            return self.responses.fallback(), FALLBACK_INTENT, prediction.confidence, False

        intent = self.dataset.intents[prediction.intent]
        slots = {}
        if intent.action:
            try:
                slots = self.actions[intent.action](message)
            except ActionError as error:
                return str(error), intent.tag, prediction.confidence, False

        text = self.responses.respond(intent.tag, slots)
        return text, intent.tag, prediction.confidence, intent.ends_conversation
