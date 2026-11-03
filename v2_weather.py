"""Weather lookup for Dora, using Open-Meteo (no API key required)."""
import json
import urllib.parse
import urllib.request


def get_weather(city="Delhi"):
    city = (city or "Delhi").strip()
    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode({
            "name": city, "count": 1, "language": "en"
        })
        with urllib.request.urlopen(geo_url, timeout=12) as response:
            geo = json.load(response)
        if not geo.get("results"):
            return f"{city} nahi mila."
        place = geo["results"][0]
        weather_url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,weather_code",
        })
        with urllib.request.urlopen(weather_url, timeout=12) as response:
            weather = json.load(response)
        current = weather["current"]
        return f"{place['name']}: {current['temperature_2m']}°C, humidity {current['relative_humidity_2m']}%"
    except Exception:
        return "Weather abhi nahi mil paya. Internet connection check karke dobara try karo."


if __name__ == "__main__":
    print(get_weather("Delhi"))
