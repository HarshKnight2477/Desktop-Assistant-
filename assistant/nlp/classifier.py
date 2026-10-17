"""Intent classifier: TF-IDF features + logistic regression."""

from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

from assistant.nlp.preprocessing import preprocess


@dataclass(frozen=True)
class Prediction:
    intent: str
    confidence: float


def build_pipeline() -> Pipeline:
    """Word n-grams capture phrasing; character n-grams tolerate typos."""
    features = FeatureUnion([
        ("words", TfidfVectorizer(preprocessor=preprocess,
                                  token_pattern=r"(?u)\b\w+\b",
                                  ngram_range=(1, 2), sublinear_tf=True)),
        ("chars", TfidfVectorizer(preprocessor=preprocess, analyzer="char_wb",
                                  ngram_range=(2, 4), sublinear_tf=True)),
    ])
    return Pipeline([
        ("features", features),
        ("model", LogisticRegression(C=10, max_iter=2000)),
    ])


class IntentClassifier:
    def __init__(self, pipeline: Pipeline | None = None):
        self.pipeline = pipeline or build_pipeline()

    def fit(self, texts: list[str], labels: list[str]) -> "IntentClassifier":
        self.pipeline.fit(texts, labels)
        return self

    def predict(self, text: str) -> Prediction:
        probabilities = self.pipeline.predict_proba([text])[0]
        best = probabilities.argmax()
        return Prediction(intent=str(self.pipeline.classes_[best]),
                          confidence=float(probabilities[best]))

    @property
    def intents(self) -> list[str]:
        return [str(c) for c in self.pipeline.classes_]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, path)

    @classmethod
    def load(cls, path: Path) -> "IntentClassifier":
        return cls(joblib.load(path))
