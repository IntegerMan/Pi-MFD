from PiMFD.Applications.Application import MFDApplication
from PiMFD.Pages.MFDPage import SimpleMessagePage
from PiMFD.Pages.WeatherPages import WeatherPage

__author__ = 'Matt Eland'


class ScheduleApp(MFDApplication):

    root_page = None
    task_page = None
    mail_page = None
    calendar_page = None
    weather_page = None

    def __init__(self, controller):

        super(ScheduleApp, self).__init__(controller)

        self.root_page = SimpleMessagePage(controller, self, self.get_button_text())

        self.task_page = SimpleMessagePage(controller, self, "TASK")
        self.mail_page = SimpleMessagePage(controller, self, "MAIL")
        self.calendar_page = SimpleMessagePage(controller, self, "CAL")
        self.weather_page = WeatherPage(controller, self)

        self.pages = list([self.task_page, self.mail_page, self.calendar_page, self.weather_page])

    def get_default_page(self):
        return self.root_page

    def get_button_text(self):
        return 'SCH'


