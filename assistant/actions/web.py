"""Browser actions: web search and opening websites."""

import webbrowser
from urllib.parse import quote_plus

from assistant.actions.base import ActionError, Slots
from assistant.actions.entities import extract_domain, extract_search_query, find_keyword

KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "mail": "https://mail.google.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "wikipedia": "https://www.wikipedia.org",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "instagram": "https://www.instagram.com",
}


def web_search(text: str) -> Slots:
    query = extract_search_query(text)
    if not query:
        raise ActionError("What would you like me to search for?")
    webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
    return {"query": query}


def open_website(text: str) -> Slots:
    domain = extract_domain(text)
    if domain:
        url = f"https://{domain}"
    else:
        url = find_keyword(text, KNOWN_SITES)
        if not url:
            raise ActionError("Which website should I open? Try \"open youtube\" or \"open github.com\".")
    webbrowser.open(url)
    return {"site": url.removeprefix("https://").removeprefix("www.")}
