import requests

from datetime import datetime

"""
Reads data from free Cat facts API
"""
class JsonReader:
    def __init__(self, base_url, api_key):
        self.url = base_url + f"?key={api_key}"
        self.api_key = api_key
        self.weatherInfo = None

    def cityWeather(self, city="Moscow"):
        response = requests.get(self.url + f"&q={city}")
        self.weatherInfo = response.json()
        return self.weatherInfo

    def H_Time(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    def TempData(self):
        temp = self.weatherInfo["current"]["temp_c"]
        cond = self.weatherInfo["current"]["condition"]["text"]
        return temp, cond

    def HistoryInfo(now, city, data):
        {
            "time": now,
            "city": city,
            "temperature": data,
            #"condition": cond
        }

