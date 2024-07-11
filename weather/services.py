import requests


class WeatherService:
    API_KEY = "8872d608e7c647ebb1121248241007"
    BASE_URL = "http://api.weatherapi.com/v1"

    @staticmethod
    def get_current_weather(location):
        url = f"{WeatherService.BASE_URL}/current.json?key={WeatherService.API_KEY}&q={location}"
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_forecast(location, days=3):
        url = f"{WeatherService.BASE_URL}/forecast.json?key={WeatherService.API_KEY}&q={location}&days={days}"
        response = requests.get(url)
        return response.json()
