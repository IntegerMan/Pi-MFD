import pywapi
from PiMFD.Data.WeatherData import WeatherData

__author__ = 'Matt Eland'


class WeatherAPI(object):

    @staticmethod
    def get_yahoo_weather(location):
        weather_data = WeatherData()
        weather_data.parse_yahoo_data(pywapi.get_weather_from_yahoo(str(location), units='imperial'))
        return weather_data