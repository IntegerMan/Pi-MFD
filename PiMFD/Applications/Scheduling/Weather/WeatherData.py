# coding=utf-8
"""
Contains data models used to insulate the weather data from the web API and used by the pages to get data in displayable
format.
"""

__author__ = 'Matt Eland'


class ForecastData(object):
    """ Contains information on a specific forecast period in format suitable for display. """

    data = None
    date = None
    day = None
    high = 'UKN'
    low = 'UKN'
    temp_range = 'Unknown'
    precipitation_chance = 'UKN'
    conditions = 'Unknown'
    code = -1

    def parse_yahoo_data(self, data, temp_suffix):
        self.data = data
        self.conditions = data["text"]
        self.high = data["high"]
        self.low = data["low"]
        self.temp_range = data["low"] + '-' + data["high"] + temp_suffix
        self.date = data["date"]
        self.day = data["day"]
        self.code = int(data["code"])


class WeatherData(object):
    """ Contains information on weather conditions that can be displayed easily in a view to users. """

    time_format = '%H:%M:%S'

    conditions = 'Unknown'
    temperature = 'UNK'
    last_result = 'No Data Available'
    windchill = 'UNK'
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
    code = -1
    forecasts = list()

    data = None

    def set_default_values(self):
        """
        Clears this instance down to its default values.
        """

        self.conditions = 'Unknown'
        self.temperature = 'UNK'
        self.last_result = 'No Data Available'
        self.windchill = 'UNK'
        self.wind_speed = 'Unknown'
        self.wind_units = ''
        self.wind_direction = 'Unknown'
        self.wind_cardinal_direction = 'Unknown'
        self.sunrise = 'Unknown'
        self.sunset = 'Unknown'
        self.humidity = 'Unknown'
        self.pressure = 'Unknown'
        self.visibility = 'Unknown'
        self.visibility_units = ''
        self.city = 'Unknown'
        self.lat = 'UNK'
        self.long = 'UNK'
        self.code = -1
        self.forecasts = list()
        self.pressure_units = ''
        self.wind_units = ''

    def parse_yahoo_data(self, yahoo_data):
        """
        Takes data from Yahoo Weather services, in the form of a dictionary, and parses it into an object that can be
        interpreted at a view level.
        :type yahoo_data: dict containing weather data
        :return: No return value.
        """

        degree_sign = u'\N{DEGREE SIGN}'

        self.data = yahoo_data

        if 'error' in yahoo_data:
            self.set_default_values()
            self.last_result = "Error: " + yahoo_data['error']
            return

        # Grab sub-collections
        condition = yahoo_data['condition']
        wind = yahoo_data['wind']
        units = yahoo_data['units']
        location = yahoo_data['location']
        atmosphere = yahoo_data['atmosphere']
        astronomy = yahoo_data['astronomy']
        geo = yahoo_data['geo']
        degree_symbol = str(units['temperature'])

        self.conditions = str(condition['text'])
        self.code = int(condition['code'])
        self.temperature = condition['temp']
        self.temp_units = degree_sign + degree_symbol
        self.sunrise = str(astronomy['sunrise'])
        self.sunset = str(astronomy['sunset'])
        self.wind_speed = wind['speed']
        self.wind_units = str(units['speed'])
        self.wind_direction = str(wind['direction']) + degree_sign
        self.wind_cardinal_direction = WeatherData.get_cardinal_direction(wind['direction'])
        self.windchill = wind['chill']
        self.city = str(location['city'])
        self.humidity = atmosphere['humidity']
        self.pressure = atmosphere['pressure']
        self.pressure_units = units['pressure']
        self.visibility_units = units['distance']
        self.visibility = atmosphere['visibility']
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
        """
        Converts degrees to a cardinal direction abbreviation (e.g. 0 is N, 45 is NE, etc.)
        :param degree: The degree to convert to a direction.
        :return: A cardinal direction abbreviation based on the degree.
        """

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


def get_condition_icon(code):
    """
    Returns the condition icon code from the condition
    :param code: The condition code
    :return: The condition icon code or a space
    """

    if code in (0, 1, 2):  # Tornado, tropical storm, hurricane
        return 'L'
    elif code in (3, 4, 37, 38, 39, 45,
                  47):  # Severe Thunderstorm, Thunderstorm, iso t-storms, scattered t-storms, thundershowers, iso thundershowers
        return 'I'
    elif code in (5, 8, 10):  # Mixed Rain / Snow, Freezing Drizzle, Freezing Rain
        return 'GH'  # Rain, Snow
    elif code in (6, 35):  # Mixed Rain / Sleet, Mixed Rain / Hail
        return 'GB'  # Rain, Sleet
    elif code == 7:  # Mixed Snow / Sleet
        return 'HB'  # Snow, Sleet
    elif code in (9, 11, 12, 40):  # Drizzle, Showers, scattered showers
        return 'G'
    elif code in (13, 14, 15, 16, 41, 42, 43,
                  46):  # Snow Flurries, light snow showers, blowing snow, snow, h. snow, sct. snow, snow showers
        return 'H'
    elif code in (17, 18):  # Hail, Sleet
        return 'B'
    elif code in (19, 20, 21, 22):  # Dust, Fog, Haze, Smoky
        return 'C'
    elif code in (23, 24):  # Blustery, Windy
        return 'L'  # TODO: This is a tornado icon, which is a bit severe for this...
    elif code == 25:  # Cold
        return ' '  # TODO: I'd like to offer a cold icon, but think snow is misinformation here
    elif code in (26, 27, 28):  # Cloudy, Mostly Cloudy (day / night)
        return 'A'
    elif code == 29:  # Partly Cloudy Night
        return 'E'
    elif code in (30, 44):  # Partly Cloudy Day, partly cloudy
        return 'F'
    elif code in (31, 33):  # Clear Night, Fair (night)
        return 'D'
    elif code in (32, 34):  # Sunny, Fair (day)
        return 'J'
    elif code == 56:  # Hot
        return 'K'

    return ' '
