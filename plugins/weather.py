import requests
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class WeatherPlugin:
    @kernel_function(
        description="Get current weather data based on latitude and longitude.",
        name="GetCurrentWeather",
    )
    def get_current_weather(
        self,
        latitude: Annotated[float, "Latitude of the location"],
        longitude: Annotated[float, "Longitude of the location"],
    ) -> str:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
        )
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            current_weather = data.get("current", {})
            temperature = current_weather.get("temperature_2m", "N/A")
            wind_speed = current_weather.get("wind_speed_10m", "N/A")

            return f"Current temperature: {temperature}°C\nWind speed: {wind_speed} m/s"
        except requests.RequestException as e:
            return "Error fetching weather information."
