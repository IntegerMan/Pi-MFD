# coding=utf-8
"""
The scheduling application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage
from PiMFD.Applications.Scheduling.Weather.WeatherDataProvider import WeatherDataProvider
from PiMFD.Applications.Scheduling.Weather.WeatherPages import WeatherPage

__author__ = 'Matt Eland'


class ScheduleApp(MFDApplication):
    """
    The scheduling application. Contains pages related to scheduling and coordinates web-service communication.
    :type controller: PiMFD.Controller.MFDController The controller.
    """
    root_page = None
    task_page = None
    mail_page = None
    calendar_page = None
    weather_page = None

    weather_data_provider = None

    def __init__(self, controller):

        super(ScheduleApp, self).__init__(controller)

        self.weather_data_provider = WeatherDataProvider(self, controller.options)

        self.root_page = SimpleMessagePage(controller, self, self.get_button_text())
        self.task_page = SimpleMessagePage(controller, self, "TASK")
        self.mail_page = SimpleMessagePage(controller, self, "MAIL")
        self.calendar_page = SimpleMessagePage(controller, self, "CAL")
        self.weather_page = WeatherPage(controller, self, self.weather_data_provider)

        self.pages = list([self.task_page, self.mail_page, self.calendar_page, self.weather_page])

    def get_default_page(self):
        """
        Gets the default page within the application.
        :return: the default page within the application.
        """
        return self.root_page

    def get_button_text(self):
        """
        Gets text for the button representing this page.
        :return: the button text for the application button.
        """
        return 'SCH'

    def page_reselected(self, page):
        """
        Handles the page reselected event for this application.
        :param page: The page that was reselected.
        """
        super(ScheduleApp, self).page_reselected(page)

        # If the user re-selects weather, refresh data
        if page is self.weather_page:
            self.weather_data_provider.get_weather()

    def handle_selected(self):
        """
        Handles the selected event for this application.
        """

        # Fetch weather data!
        self.weather_data_provider.get_weather()

    def initialize(self):
        super(ScheduleApp, self).initialize()
        
        self.controller.register_data_provider(self.weather_data_provider)

    


