import random

import pytest

from assistant.actions import ActionError
from assistant.chatbot import FALLBACK_INTENT, Chatbot
from assistant.responses import ResponseEngine


def fake_search(text):
    return {"query": "cats"}


def failing_search(text):
    raise ActionError("What would you like me to search for?")


@pytest.fixture
def make_bot(classifier, dataset):
    def make(actions=None, threshold=0.3):
        responses = ResponseEngine(dataset, rng=random.Random(0))
        return Chatbot(classifier, dataset, actions=actions or {}, threshold=threshold,
                       responses=responses)
    return make


def test_reply_for_simple_intent(make_bot, dataset):
    reply = make_bot().reply("hello")
    assert reply.intent == "greeting"
    assert reply.text in dataset.intents["greeting"].responses
    assert reply.latency_ms >= 0


def test_action_slots_fill_the_response(make_bot):
    reply = make_bot(actions={"web_search": fake_search}).reply("search for cats")
    assert reply.intent == "web_search"
    assert '"cats"' in reply.text


def test_action_error_becomes_the_reply(make_bot):
    reply = make_bot(actions={"web_search": failing_search}).reply("search for cats")
    assert reply.text == "What would you like me to search for?"


def test_low_confidence_falls_back(make_bot, dataset):
    reply = make_bot(threshold=1.01).reply("hello")
    assert reply.intent == FALLBACK_INTENT
    assert reply.text in dataset.fallback


def test_empty_message_falls_back(make_bot):
    assert make_bot().reply("   ").intent == FALLBACK_INTENT


def test_goodbye_ends_conversation(make_bot):
    assert make_bot().reply("bye").ends_conversation
    assert not make_bot().reply("hello").ends_conversation


def test_identity_uses_assistant_name(make_bot):
    from assistant import config
    assert config.ASSISTANT_NAME in make_bot().reply("what is your name").text
