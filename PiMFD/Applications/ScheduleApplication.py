from PiMFD.Applications.Application import MFDApplication
from PiMFD.Data.WeatherAPIWrapper import WeatherAPI
from PiMFD.Data.WeatherData import WeatherData
from PiMFD.Pages.MFDPage import SimpleMessagePage
from PiMFD.Pages.WeatherPages import WeatherPage

__author__ = 'Matt Eland'


class ScheduleApp(MFDApplication):

    root_page = None
    task_page = None
    mail_page = None
    calendar_page = None
    weather_page = None

    weather_data = WeatherData()
    weather_api = WeatherAPI()

    def __init__(self, controller):

        super(ScheduleApp, self).__init__(controller)

        self.root_page = SimpleMessagePage(controller, self, self.get_button_text())

        self.task_page = SimpleMessagePage(controller, self, "TASK")
        self.mail_page = SimpleMessagePage(controller, self, "MAIL")
        self.calendar_page = SimpleMessagePage(controller, self, "CAL")
        self.weather_page = WeatherPage(controller, self)

        self.pages = list([self.task_page, self.mail_page, self.calendar_page, self.weather_page])

        self.get_weather()

    def get_weather(self):
        self.weather_data = self.weather_api.get_yahoo_weather(self.controller.location)

    def get_default_page(self):
        return self.root_page

    def get_button_text(self):
        return 'SCH'



