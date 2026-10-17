"""Action registry: maps the ``action`` name used in intents.json to a function."""

from assistant.actions.base import Action, ActionError, Slots
from assistant.actions.system import close_app, open_app, open_folder, tell_date, tell_joke, tell_time
from assistant.actions.weather import get_weather
from assistant.actions.web import open_website, web_search

DEFAULT_ACTIONS: dict[str, Action] = {
    "tell_time": tell_time,
    "tell_date": tell_date,
    "tell_joke": tell_joke,
    "get_weather": get_weather,
    "web_search": web_search,
    "open_website": open_website,
    "open_app": open_app,
    "close_app": close_app,
    "open_folder": open_folder,
}

__all__ = ["Action", "ActionError", "Slots", "DEFAULT_ACTIONS"]
