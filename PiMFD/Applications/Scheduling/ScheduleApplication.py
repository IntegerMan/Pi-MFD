# coding=utf-8
"""
The scheduling application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage
from PiMFD.Applications.Scheduling.Weather.WeatherAPIWrapper import WeatherAPI
from PiMFD.Applications.Scheduling.Weather.WeatherData import WeatherData
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

    weather_data = WeatherData()
    weather_api = WeatherAPI()

    def __init__(self, controller):

        super(ScheduleApp, self).__init__(controller)

        self.root_page = SimpleMessagePage(controller, self, self.get_button_text())

        self.task_page = SimpleMessagePage(controller, self, "TASK")
        self.mail_page = SimpleMessagePage(controller, self, "MAIL")
        self.calendar_page = SimpleMessagePage(controller, self, "CAL")
        self.weather_page = WeatherPage(controller, self, self)

        self.pages = list([self.task_page, self.mail_page, self.calendar_page, self.weather_page])

        # TODO: There's no automatic mechanism to refresh weather data.
        # TODO: This should be in another thread so the UI can keep rendering
        self.get_weather()

    def get_weather(self):
        """
        Gets weather data from the weather API (Yahoo Weather) and stores it for the weather page.
        """

        if self.controller.options.location:
            weather = self.get_weather_for_zip(self.controller.options.location, updateError=True)
            if weather:
                self.weather_data = weather

    def get_weather_for_zip(self, zip, updateError=False):

        try:
            # TODO: I might want to impose some frequency restrictions here
            return self.weather_api.get_yahoo_weather(zip)
        except Exception as exception:

            if updateError:
                self.weather_data.last_result = 'Could not get weather: ' + exception.message

            return None


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
            self.get_weather()

    def handle_selected(self):
        """
        Handles the selected event for this application.
        """

        # Fetch weather data!
        self.get_weather()




