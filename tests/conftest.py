import pytest

from assistant.data_loader import load_intents
from assistant.nlp import IntentClassifier


@pytest.fixture(scope="session")
def dataset():
    return load_intents()


@pytest.fixture(scope="session")
def classifier(dataset):
    texts, labels = dataset.training_data()
    return IntentClassifier().fit(texts, labels)
