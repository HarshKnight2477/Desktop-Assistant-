import pytest

from assistant.actions.entities import extract_city, extract_domain, extract_search_query, find_keyword


@pytest.mark.parametrize("text, query", [
    ("search python tutorials", "python tutorials"),
    ("Search for best laptops", "best laptops"),
    ("google how to cook rice", "how to cook rice"),
    ("look up the population of india", "the population of india"),
    ("can you google cricket score", "cricket score"),
    ("search the web for news", "news"),
    ("find cheap flights online", "cheap flights"),
    ("search", ""),
    ("﻿search", ""),
    ("google for", ""),
])
def test_extract_search_query(text, query):
    assert extract_search_query(text) == query


@pytest.mark.parametrize("text, city", [
    ("weather in mumbai", "Mumbai"),
    ("what's the temperature in New York today?", "New York"),
    ("is it raining in chennai", "Chennai"),
    ("what's the weather", None),
    ("is it cold outside", None),
])
def test_extract_city(text, city):
    assert extract_city(text) == city


def test_web_search_without_query_asks_instead_of_opening_browser(monkeypatch):
    from assistant.actions import web
    from assistant.actions.base import ActionError
    opened = []
    monkeypatch.setattr(web.webbrowser, "open", opened.append)
    with pytest.raises(ActionError):
        web.web_search("search")
    assert opened == []


def test_extract_domain():
    assert extract_domain("open the website github.com") == "github.com"
    assert extract_domain("open youtube") is None


def test_find_keyword_prefers_longest_match():
    keywords = {"explorer": "short", "file explorer": "long"}
    assert find_keyword("open file explorer", keywords) == "long"
    assert find_keyword("open notepad", keywords) is None
