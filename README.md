# Desktop Assistant

A Python desktop assistant with an NLP chatbot at its core. It understands plain-English text or voice commands, classifies them into intents, and either replies or acts: searching the web, checking live weather, opening websites, apps and folders, and more.

```
You: weather in pune
Jarvis: It's 33°C and mainly clear in Pune (wind 9 km/h).
You: open notepad
Jarvis: Opening Notepad.
You: search for python tutorials
Jarvis: Searching the web for "python tutorials".
```

## How it works

```
message ─► preprocessing ─► TF-IDF vectors ─► intent classifier ─► action ─► response
           tokenize          word 1-2 grams    logistic regression   (slots)   template
           drop filler       + char 2-4 grams  + confidence score
           Porter stemming
```

1. **Preprocessing** (`assistant/nlp/preprocessing.py`): lowercases, tokenizes, removes politeness filler ("could you please…") and stems words with NLTK's Porter stemmer, so "opening", "opens" and "open" look the same.
2. **Vectorization + classification** (`assistant/nlp/classifier.py`): a scikit-learn pipeline combines word n-grams (phrasing) with character n-grams (typo tolerance, e.g. "wats the wether") and feeds them to a logistic regression model that returns an intent and a confidence.
3. **Confidence threshold**: below 0.30 confidence the bot asks you to rephrase instead of guessing.
4. **Actions** (`assistant/actions/`): intents like `weather` or `open_app` run an action that extracts what it needs from the message (city, search query, app name) and returns slots.
5. **Responses** (`assistant/responses.py`): a template for the intent is filled with those slots ("It's {temperature}°C in {city}"). If an action can't finish, it explains why ("Which city?").

## Results

Measured with `python -m assistant.evaluate`. The full report, including per-intent scores, is in [`reports/evaluation.md`](reports/evaluation.md).

| Metric | Value |
|---|---|
| Intents | 15 |
| Training samples | 337 |
| Held-out test accuracy (60 phrases never seen in training) | **93.3%** (macro F1 0.933) |
| 5-fold cross-validation accuracy | 79.8% (macro F1 0.797) |
| Mean classification latency | under 1 ms |

## Supported intents

| Intent | Example | What happens |
|---|---|---|
| greeting / goodbye / thanks | "hi", "bye", "thanks" | Conversational reply; "bye" ends the session |
| identity / capabilities / wellbeing | "who are you", "help", "how are you" | Describes the assistant and its commands |
| joke | "tell me a joke" | Tells a programming joke |
| time / date | "what time is it", "what's today's date" | Reads the system clock |
| weather | "weather in Mumbai" | Live weather from [Open-Meteo](https://open-meteo.com) (no API key) |
| web_search | "search for best laptops" | Opens a Google search |
| open_website | "open youtube", "open github.com" | Opens the site in your browser |
| open_app / close_app | "open notepad", "close calculator" | Starts or closes allowlisted Windows apps |
| open_folder | "open downloads" | Opens Downloads, Documents, Desktop, Pictures, Music or Videos |

Only allowlisted apps can be opened or closed, and closing never force-kills, so unsaved work still gets a "Save?" prompt.

## Getting started

Requires Python 3.10+. App control is Windows-only; everything else works on any OS.

```bash
git clone https://github.com/HarshKnight2477/Desktop-Assistant-.git
cd Desktop-Assistant-
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Run it:

```bash
python -m assistant             # text chat
python -m assistant --debug     # also show intent, confidence and latency
python -m assistant --voice     # voice chat (see below)
```

The model trains automatically on first run. To retrain or re-measure after editing the data:

```bash
python -m assistant.train
python -m assistant.evaluate
```

### Voice mode

```bash
pip install -r requirements-voice.txt
python -m assistant --voice
```

Uses your microphone with Google speech recognition (needs internet) and speaks replies with `pyttsx3`.

### Configuration

| Environment variable | Default | Purpose |
|---|---|---|
| `ASSISTANT_NAME` | `Jarvis` | Name the assistant uses |
| `ASSISTANT_CITY` | none | City for "what's the weather" when none is named |
| `ASSISTANT_CONFIDENCE` | `0.30` | Minimum confidence before falling back |

## Project structure

```
assistant/
├── __main__.py          # entry point: python -m assistant
├── config.py            # paths and settings
├── chatbot.py           # classify → act → respond
├── responses.py         # response templates and fallback
├── data_loader.py       # loads and validates intents.json
├── train.py             # trains and saves the model
├── evaluate.py          # cross-validation + held-out test report
├── data/
│   ├── intents.json     # intents: patterns, responses, actions
│   └── test_phrases.json# held-out evaluation phrases
├── nlp/
│   ├── preprocessing.py # tokenize, filler removal, stemming
│   └── classifier.py    # TF-IDF + logistic regression
├── actions/
│   ├── entities.py      # extracts city, query, app, folder
│   ├── web.py           # web search, open websites
│   ├── weather.py       # Open-Meteo weather
│   └── system.py        # time, date, jokes, apps, folders
└── interfaces/
    ├── cli.py           # text chat
    └── voice.py         # speech in, speech out
tests/                   # pytest suite
reports/evaluation.md    # latest evaluation results
```

## Adding a new intent

1. Add an entry to `assistant/data/intents.json` with a `tag`, at least 10 `patterns` and some `responses`.
2. If it needs to *do* something, write a function in `assistant/actions/` that takes the message and returns slots, then register it in `assistant/actions/__init__.py` and set `"action"` on the intent.
3. Run `python -m assistant.train`, then `python -m pytest` and `python -m assistant.evaluate`.

## Running tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The tests cover preprocessing, classification, slot extraction and chatbot behaviour, and they check that every response placeholder is always filled and that no test phrase leaks into the training data.
