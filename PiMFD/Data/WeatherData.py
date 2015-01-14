from time import strftime

__author__ = 'Matt Eland'


class WeatherData(object):

    time_format = '%H:%M:%S'
    degree_unit = 'F'

    current_conditions = 'Unknown'
    current_temperature = 'Unknown'
    last_result = 'No Weather Data Available'

    yahoo_data = None

    def parse_yahoo_data(self, yahoo_data):

        degree_sign = u'\N{DEGREE SIGN}'

        self.yahoo_data = yahoo_data

        self.current_conditions = str(yahoo_data['condition']['text'])
        self.current_temperature = str(yahoo_data['condition']['temp']) + degree_sign + self.degree_unit
        self.last_result = 'Weather as of ' + strftime(self.time_format)
