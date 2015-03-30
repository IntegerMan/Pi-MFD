from threading import Thread

from suds.client import Client


try:
    import pywapi
except ImportError:
    pywapi = None

from PiMFD.Applications.Scheduling.Weather.WeatherData import WeatherData


__author__ = 'Matt Eland'


class WeatherFetchThread(Thread):
    def __init__(self, location, consumer, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(WeatherFetchThread, self).__init__(group, target, name, args, kwargs, verbose)

        self.location = location
        self.consumer = consumer

    def run(self):
        super(WeatherFetchThread, self).run()

        if self.consumer:
            weather = WeatherAPI.get_yahoo_weather(self.location)

            if weather:
                self.consumer.weather_received(self.location, weather)


class WeatherAPI(object):

    @staticmethod
    def get_ani_weather(location):
        print('fetching ANI weather data for ' + location)
        client = Client("http://www.matteland.com/ANIServices/AniService.svc?wsdl")
        data = client.service.GetWeatherData(location)

        weather_data = WeatherData()
        weather_data.parse_ani_data(data)

        return weather_data

    @staticmethod
    def get_yahoo_weather(location):

        if not pywapi:
            return None

        print('fetching Yahoo weather data for ' + location)

        weather_data = WeatherData()
        weather_data.parse_yahoo_data(pywapi.get_weather_from_yahoo(str(location), units='imperial'))
        return weather_data

    @staticmethod
    def get_weather_async(location, consumer):
        thread = WeatherFetchThread(location, consumer)
        thread.start()
