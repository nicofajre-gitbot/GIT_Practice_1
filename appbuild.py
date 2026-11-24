import json
import sys
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


CITIES = (
    "Buenos Aires",
    "São Paulo",
    "New York",
    "London",
    "Tokyo",
    "Paris",
    "Cairo",
    "Mumbai",
    "Sydney",
    "Mexico City",
)

WEATHER_CODES = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail",
}


def fetch_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=20) as response:
        return json.load(response)


def get_city_weather(city: str) -> list[str]:
    geocoding_url = (
        "https://geocoding-api.open-meteo.com/v1/search?"
        + urlencode(
            {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            }
        )
    )
    locations = fetch_json(geocoding_url).get("results", [])
    if not locations:
        return [city, "-", "-", "-", "-", "Not found"]

    location = locations[0]
    forecast_url = (
        "https://api.open-meteo.com/v1/forecast?"
        + urlencode(
            {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "weather_code,wind_speed_10m"
                ),
                "temperature_unit": "celsius",
                "wind_speed_unit": "kmh",
                "timezone": "auto",
            }
        )
    )
    current = fetch_json(forecast_url)["current"]
    code = current["weather_code"]

    return [
        location.get("name", city),
        location.get("country", "-"),
        f"{current['temperature_2m']:.1f}",
        str(current["relative_humidity_2m"]),
        f"{current['wind_speed_10m']:.1f}",
        WEATHER_CODES.get(code, f"Weather code {code}"),
    ]


def print_table(rows: list[list[str]]) -> None:
    headers = ["City", "Country", "Temp (C)", "Humidity (%)", "Wind (km/h)", "Conditions"]
    table = [headers, *rows]
    widths = [
        max(len(row[index]) for row in table)
        for index in range(len(headers))
    ]

    for row_index, row in enumerate(table):
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))
        if row_index == 0:
            print("-+-".join("-" * width for width in widths))


def main() -> None:
    rows = []
    for city in CITIES:
        try:
            rows.append(get_city_weather(city))
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"Could not fetch weather for {city}: {error}", file=sys.stderr)
            rows.append([city, "-", "-", "-", "-", "Request failed"])

    print_table(rows)


if __name__ == "__main__":
    main()