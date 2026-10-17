"""Central configuration. Values can be overridden with environment variables."""

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent

INTENTS_PATH = PACKAGE_DIR / "data" / "intents.json"
TEST_PHRASES_PATH = PACKAGE_DIR / "data" / "test_phrases.json"
MODEL_PATH = PROJECT_DIR / "models" / "intent_model.joblib"
REPORT_PATH = PROJECT_DIR / "reports" / "evaluation.md"

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")

# Below this confidence the bot asks the user to rephrase instead of guessing.
CONFIDENCE_THRESHOLD = float(os.getenv("ASSISTANT_CONFIDENCE", "0.30"))

# City used for "what's the weather" when the user doesn't name one.
DEFAULT_CITY = os.getenv("ASSISTANT_CITY", "")

HTTP_TIMEOUT_SECONDS = 6
