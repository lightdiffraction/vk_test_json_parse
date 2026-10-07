import json
import urllib.request
from dataclasses import dataclass
from collections import defaultdict

url = "https://wttr.in/"

@dataclass
class Temperature:
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        if self.value > 0:
            return f"+{self.value:g} °C"
        else:
            return f"{self.value:g} °C"
        
@dataclass
class WeatherData():
    city: str
    temperature: Temperature
    country: str
    def __str__(self):
        return f"{self.city}, {self.country} {self.temperature}"

country_dict = defaultdict(list)

with open("Cities.txt", "r", encoding="utf-8-sig") as f:
    for line in f:
        try:
            with urllib.request.urlopen(f"{url}{line.strip()}?format=j1") as response:
                data = json.load(response)
                weather_data = WeatherData(
                    city=line.strip(),
                    temperature=Temperature(float(data["current_condition"][0]["temp_C"])),
                    country=data["nearest_area"][0]["country"][0]["value"]
                )
                country_dict[weather_data.country].append(weather_data)
                print(weather_data)
        except Exception as e:
            print(f"Error fetching data for {line.strip()}: {e}")
for country, weather_data_list in country_dict.items():
    current_min_temp = weather_data_list[0].temperature.value
    current_max_temp = weather_data_list[0].temperature.value
    temp_sum = 0
    for weather_data in weather_data_list:
        if weather_data.temperature.value < current_min_temp:
            current_min_temp = weather_data.temperature.value
        if weather_data.temperature.value > current_max_temp:
            current_max_temp = weather_data.temperature.value
        temp_sum += weather_data.temperature.value

        ''' еще можно сделать вот так чтобы было короче, но тогда больше сложность по времени т.к проходить по массиву несколько раз
        temps = [wd.temperature.value for wd in weather_data_list]
        avg_temp = sum(temps) / len(temps)
        min_temp = min(temps)
        max_temp = max(temps)'''
    print(f"{country} - {len(weather_data_list)} cities, avg: {Temperature(temp_sum / len(weather_data_list))}, min: {Temperature(current_min_temp)}, max: {Temperature(current_max_temp)}")