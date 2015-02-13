try:
    import pywapi
except ImportError:
    pywapi = None

from PiMFD.Applications.Scheduling.Weather.WeatherData import WeatherData


__author__ = 'Matt Eland'


class WeatherAPI(object):

    @staticmethod
    def get_yahoo_weather(location):

        if not pywapi:
            return None

        weather_data = WeatherData()
        weather_data.parse_yahoo_data(pywapi.get_weather_from_yahoo(str(location), units='imperial'))
        return weather_data