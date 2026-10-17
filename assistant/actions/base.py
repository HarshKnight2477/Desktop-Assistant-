"""Shared types for actions.

An action receives the raw user message, does its work, and returns the
slots (``{"time": "10:30 AM"}``) used to fill the intent's response template.
When it can't finish, it raises ``ActionError`` with a message for the user.
"""

from typing import Callable

Slots = dict[str, str]
Action = Callable[[str], Slots]


class ActionError(Exception):
    """Raised by an action; its message is shown to the user as the reply."""
