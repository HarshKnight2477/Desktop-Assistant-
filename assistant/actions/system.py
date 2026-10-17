"""Desktop actions: time/date, jokes, apps and folders.

Only apps and folders in the allowlists below can be opened or closed, so a
misheard command can never launch or kill anything unexpected.
"""

import os
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from assistant.actions.base import ActionError, Slots
from assistant.actions.entities import find_keyword

# spoken name -> (display name, command to launch, process image to close)
APPS = {
    "notepad": ("Notepad", ["notepad.exe"], "notepad.exe"),
    "calculator": ("Calculator", ["calc.exe"], "CalculatorApp.exe"),
    "calc": ("Calculator", ["calc.exe"], "CalculatorApp.exe"),
    "paint": ("Paint", ["mspaint.exe"], "mspaint.exe"),
    "file explorer": ("File Explorer", ["explorer.exe"], None),
    "explorer": ("File Explorer", ["explorer.exe"], None),
    "command prompt": ("Command Prompt", ["cmd.exe", "/c", "start", "cmd.exe"], None),
    "cmd": ("Command Prompt", ["cmd.exe", "/c", "start", "cmd.exe"], None),
    "terminal": ("Terminal", ["wt.exe"], None),
    "task manager": ("Task Manager", ["taskmgr.exe"], None),
}
_APP_KEYWORDS = {name: name for name in APPS}

FOLDERS = {
    name: name.title()
    for name in ("downloads", "documents", "desktop", "pictures", "music", "videos")
}
FOLDERS |= {"download": "Downloads", "document": "Documents", "picture": "Pictures",
            "photos": "Pictures", "video": "Videos"}

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and it said: 'No problem, I'll go to sleep.'",
    "Why did the Python developer wear glasses? Because they couldn't C.",
    "There are 10 kinds of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
    "Debugging is like being the detective in a crime movie where you're also the murderer.",
]


def tell_time(_: str) -> Slots:
    return {"time": datetime.now().strftime("%I:%M %p").lstrip("0")}


def tell_date(_: str) -> Slots:
    now = datetime.now()
    return {"date": f"{now:%A}, {now.day} {now:%B %Y}"}


def tell_joke(_: str) -> Slots:
    return {"joke": random.choice(JOKES)}


def _require_windows() -> None:
    if sys.platform != "win32":
        raise ActionError("Opening and closing apps is only set up for Windows right now.")


def _find_app(text: str) -> tuple[str, list[str], str | None]:
    name = find_keyword(text, _APP_KEYWORDS)
    if not name:
        supported = ", ".join(sorted({display for display, _, _ in APPS.values()}))
        raise ActionError(f"I can only manage these apps: {supported}.")
    return APPS[name]


def open_app(text: str) -> Slots:
    display, command, _ = _find_app(text)
    _require_windows()
    try:
        subprocess.Popen(command)
    except OSError:
        raise ActionError(f"I couldn't start {display}.")
    return {"app": display}


def close_app(text: str) -> Slots:
    display, _, image = _find_app(text)
    if image is None:
        raise ActionError(f"For safety, I don't close {display}. Please close it yourself.")
    _require_windows()
    # No /F: apps close normally, so unsaved work still triggers a "Save?" prompt.
    result = subprocess.run(["taskkill", "/IM", image], capture_output=True, text=True)
    if result.returncode != 0:
        raise ActionError(f"{display} doesn't seem to be running.")
    return {"app": display}


def open_folder(text: str) -> Slots:
    folder = find_keyword(text, FOLDERS)
    if not folder:
        raise ActionError("Which folder? I know Downloads, Documents, Desktop, Pictures, Music and Videos.")
    path = Path.home() / folder
    if not path.is_dir():
        raise ActionError(f"I couldn't find your {folder} folder.")
    if sys.platform == "win32":
        os.startfile(path)
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", str(path)])
    return {"folder": folder}
