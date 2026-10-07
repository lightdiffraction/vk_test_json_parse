import json
import urllib.request
from dataclasses import dataclass
url = "https://wttr.in/"

@dataclass
class WeatherData:
    city: str
    temperature: int
    country: str


with open("Cities.txt", "r", encoding="utf-8-sig") as f:
    data = f.readlines()
for line in data:
    with urllib.request.urlopen(f"{url}{line.strip()}?format=j1") as response:
        data = json.load(response)
        weather_data = WeatherData(
            city=data["nearest_area"][0]["areaName"][0]["value"],
            temperature=int(data["current_condition"][0]["temp_C"]),
            country=data["nearest_area"][0]["country"][0]["value"]
        )
        print(weather_data)