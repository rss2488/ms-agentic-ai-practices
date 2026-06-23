import requests
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class LocationPlugin:
    @kernel_function(
        description="Get location details like city, country, coordinates, and timezone based on current IP address.",
        name="GetLocationInfo",
    )
    def get_location_info(self) -> str:
        url = "https://ipinfo.io/json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            city = data.get("city", "Unknown city")
            region = data.get("region", "Unknown region")
            country = data.get("country", "Unknown country")
            loc = data.get("loc", "Unknown coordinates")
            timezone = data.get("timezone", "Unknown timezone")

            return (
                f"{city}, {region}, {country}\nCoordinates: {loc}\nTimezone: {timezone}"
            )
        except requests.RequestException as e:
            return "Error fetching location information."

    @kernel_function(
        description="Extract latitude and longitude from a loc string in 'latitude,longitude' format.",
        name="GetLatLonFromLoc",
    )
    def get_lat_lon_from_loc(
        self,
        loc: Annotated[str, "Coordinates string in 'latitude,longitude' format"],
    ) -> str:
        try:
            lat, lon = loc.split(",")
            return f"Latitude: {lat.strip()}, Longitude: {lon.strip()}"
        except ValueError:
            return "Invalid loc format. Expected 'latitude,longitude'."
