import requests
from .config import get_amap_key

AMAP_KEY = get_amap_key()


def get_weather(city: str) -> dict:
    """Query weather API for a city. Returns forecast data."""
    try:
        # Use wttr.in - a free, no-key weather API
        resp = requests.get(
            f"https://wttr.in/{city}?format=j1",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        data = resp.json()

        forecasts = []
        weather_data = data.get("weather", [])
        for day_data in weather_data[:7]:  # up to 7 days
            hourly = day_data.get("hourly", [])
            day_weather = ""
            night_weather = ""
            day_temp = ""
            night_temp = ""
            day_wind = ""
            day_power = ""

            if hourly:
                # Morning/afternoon (around 14:00)
                mid_idx = min(len(hourly) // 2, len(hourly) - 1)
                mid = hourly[mid_idx]
                day_weather = mid.get("weatherDesc", [{}])[0].get("value", "")
                day_temp = mid.get("tempC", "")
                wind_speed = mid.get("windspeedKmph", "")
                wind_dir = mid.get("winddir16Point", "")
                if wind_speed:
                    day_wind = f"{wind_dir}"
                    day_power = wind_speed

                # Night (around 2:00)
                early = hourly[min(2, len(hourly) - 1)]
                night_weather = early.get("weatherDesc", [{}])[0].get("value", "")
                night_temp = early.get("tempC", "")

            forecasts.append({
                "date": day_data.get("date", ""),
                "day_weather": day_weather,
                "night_weather": night_weather,
                "day_temp": day_temp,
                "night_temp": night_temp,
                "day_wind": day_wind,
                "night_wind": "",
                "day_power": day_power,
                "night_power": "",
            })

        return {
            "city": city,
            "forecasts": forecasts,
        }

    except requests.RequestException as e:
        return {"error": f"????????: {str(e)}"}
    except Exception as e:
        return {"error": f"??????: {str(e)}"}


def format_weather_alert(forecast: dict) -> str:
    """Format a single day's forecast into weather_alert string."""
    day = forecast.get("day_weather", "")
    night = forecast.get("night_weather", "")
    day_temp = forecast.get("day_temp", "")
    night_temp = forecast.get("night_temp", "")
    day_wind = forecast.get("day_wind", "")
    day_power = forecast.get("day_power", "")

    parts = [f"??{day} {day_temp}°C", f"??{night} {night_temp}°C"]
    if day_wind:
        parts.append(f"{day_wind} {day_power}km/h")

    return "，".join(parts)
