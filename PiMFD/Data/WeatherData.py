from time import strftime

__author__ = 'Matt Eland'


class ForecastData(object):

    data = None
    date = None
    day = None
    high = 'UKN'
    low = 'UKN'
    temp_range = 'Unknown'
    precipitation_chance = 'UKN'

    def parse_yahoo_data(self, data, temp_suffix):
        self.data = data
        self.conditions = data["text"]
        self.high = data["high"] + temp_suffix
        self.low = data["low"] + temp_suffix
        self.temp_range = data["low"] + '-' + data["high"] + temp_suffix
        self.date = data["date"]
        self.day = data["day"]


class WeatherData(object):

    time_format = '%H:%M:%S'

    conditions = 'Unknown'
    temperature = 'Unknown'
    last_result = 'No Data Available'
    windchill = 'Unknown'
    wind_speed = 'Unknown'
    wind_direction = 'Unknown'
    wind_cardinal_direction = 'Unknown'
    sunrise = 'Unknown'
    sunset = 'Unknown'
    humidity = 'Unknown'
    pressure = 'Unknown'
    visibility = 'Unknown'
    city = 'Unknown'
    lat = 'UNK'
    long = 'UNK'
    forecasts = list()

    data = None

    def parse_yahoo_data(self, yahoo_data):

        degree_sign = u'\N{DEGREE SIGN}'

        self.data = yahoo_data

        degree_symbol = str(yahoo_data['units']['temperature'])

        # Grab sub-collections
        condition = yahoo_data['condition']
        wind = yahoo_data['wind']
        units = yahoo_data['units']
        location = yahoo_data['location']
        atmosphere = yahoo_data['atmosphere']
        astronomy = yahoo_data['astronomy']
        geo = yahoo_data['geo']

        # TODO: This really needs to be safer with possibly excluded results
        self.conditions = str(condition['text'])
        self.temperature = str(condition['temp']) + degree_sign + degree_symbol
        self.sunrise = str(astronomy['sunrise'])
        self.sunset = str(astronomy['sunset'])
        self.wind_speed = str(wind['speed']) + ' ' + str(units['speed'])
        self.wind_direction = str(wind['direction']) + degree_sign
        self.wind_cardinal_direction = WeatherData.get_cardinal_direction(wind['direction'])
        self.windchill = str(wind['chill']) + degree_sign + degree_symbol
        self.city = str(location['city'])
        self.humidity = str(atmosphere['humidity']) + ' %'
        self.pressure = str(atmosphere['pressure']) + ' ' + units['pressure']
        self.visibility = str(atmosphere['visibility']) + ' ' + units['distance']
        self.last_result = str(condition['date'])
        self.lat = str(geo['lat']) + degree_sign
        self.long = str(geo['long']) + degree_sign

        # Interpret forecasts
        self.forecasts = list()
        for forecast_data in yahoo_data['forecasts']:
            forecast = ForecastData()
            forecast.parse_yahoo_data(forecast_data, degree_sign + degree_symbol)
            self.forecasts.append(forecast)


    @staticmethod
    def get_cardinal_direction(degree):

        # Based on http://climate.umn.edu/snow_fence/Components/winddirectionanddegreeswithouttable3.htm
        if degree <= 11.25:
            return 'N'
        elif degree <= 33.75:
            return 'NNE'
        elif degree <= 56.25:
            return 'NE'
        elif degree <= 78.75:
            return 'ENE'
        elif degree <= 101.25:
            return 'E'
        elif degree <= 123.75:
            return 'ESE'
        elif degree <= 146.25:
            return 'SE'
        elif degree <= 168.75:
            return 'SSE'
        elif degree <= 191.25:
            return 'S'
        elif degree <= 213.75:
            return 'SSW'
        elif degree <= 236.25:
            return 'SW'
        elif degree <= 258.75:
            return 'WSW'
        elif degree <= 281.25:
            return 'W'
        elif degree <= 303.75:
            return 'WNW'
        elif degree <= 326.25:
            return 'NW'
        elif degree <= 348.75:
            return 'NNW'
        else:
            return 'N'