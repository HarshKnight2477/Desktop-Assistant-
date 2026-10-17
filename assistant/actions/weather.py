"""Live weather from the free Open-Meteo API (no API key needed)."""

import requests

from assistant import config
from assistant.actions.base import ActionError, Slots
from assistant.actions.entities import extract_city

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO weather interpretation codes -> plain words.
WEATHER_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "foggy", 51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
    61: "light rain", 63: "rain", 65: "heavy rain", 71: "light snow", 73: "snow",
    75: "heavy snow", 80: "rain showers", 81: "rain showers", 82: "heavy rain showers",
    95: "thunderstorms", 96: "thunderstorms with hail", 99: "thunderstorms with hail",
}


def get_weather(text: str) -> Slots:
    city = extract_city(text) or config.DEFAULT_CITY
    if not city:
        raise ActionError("Which city? Try \"weather in Mumbai\" "
                          "(or set the ASSISTANT_CITY environment variable).")
    try:
        place = _geocode(city)
        current = _current_weather(place["latitude"], place["longitude"])
    except requests.RequestException:
        raise ActionError("I couldn't reach the weather service. Check your internet connection.")

    return {
        "city": place["name"],
        "temperature": f"{current['temperature_2m']:.0f}",
        "condition": WEATHER_CODES.get(current["weather_code"], "unknown conditions"),
        "wind": f"{current['wind_speed_10m']:.0f}",
    }


def _geocode(city: str) -> dict:
    response = requests.get(GEOCODE_URL, params={"name": city, "count": 1},
                            timeout=config.HTTP_TIMEOUT_SECONDS)
    response.raise_for_status()
    results = response.json().get("results")
    if not results:
        raise ActionError(f"I couldn't find a place called {city}.")
    return results[0]


def _current_weather(latitude: float, longitude: float) -> dict:
    response = requests.get(FORECAST_URL, params={
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m",
    }, timeout=config.HTTP_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()["current"]
