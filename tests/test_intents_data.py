from assistant.actions import DEFAULT_ACTIONS
from assistant.data_loader import load_test_phrases
from assistant.responses import template_fields

SLOTS_FROM_ACTIONS = {
    "tell_time": {"time"},
    "tell_date": {"date"},
    "tell_joke": {"joke"},
    "get_weather": {"city", "temperature", "condition", "wind"},
    "web_search": {"query"},
    "open_website": {"site"},
    "open_app": {"app"},
    "close_app": {"app"},
    "open_folder": {"folder"},
}


def test_every_action_is_registered(dataset):
    for intent in dataset.intents.values():
        if intent.action:
            assert intent.action in DEFAULT_ACTIONS, intent.tag


def test_response_placeholders_are_always_filled(dataset):
    for intent in dataset.intents.values():
        available = {"assistant_name"} | SLOTS_FROM_ACTIONS.get(intent.action, set())
        for template in intent.responses:
            assert template_fields(template) <= available, (intent.tag, template)


def test_each_intent_has_enough_patterns(dataset):
    for intent in dataset.intents.values():
        assert len(intent.patterns) >= 10, intent.tag


def test_held_out_phrases_are_not_in_training_data(dataset):
    training = {p.lower() for i in dataset.intents.values() for p in i.patterns}
    for text, tag in load_test_phrases():
        assert text.lower() not in training, text
        assert tag in dataset.intents, tag
