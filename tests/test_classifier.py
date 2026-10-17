import pytest

from assistant.nlp import IntentClassifier


@pytest.mark.parametrize("text, intent", [
    ("hello there", "greeting"),
    ("what time is it", "time"),
    ("what's the weather in paris", "weather"),
    ("search for python books", "web_search"),
    ("open youtube", "open_website"),
    ("open notepad", "open_app"),
    ("close notepad", "close_app"),
    ("open my downloads folder", "open_folder"),
    ("bye", "goodbye"),
])
def test_predicts_expected_intent(classifier, text, intent):
    assert classifier.predict(text).intent == intent


def test_confidence_is_a_probability(classifier):
    confidence = classifier.predict("tell me a joke").confidence
    assert 0.0 < confidence <= 1.0


def test_tolerates_small_typos(classifier):
    assert classifier.predict("wats the wether in delhi").intent == "weather"


def test_save_and_load_round_trip(classifier, tmp_path):
    path = tmp_path / "model.joblib"
    classifier.save(path)
    loaded = IntentClassifier.load(path)
    assert loaded.predict("good morning") == classifier.predict("good morning")
