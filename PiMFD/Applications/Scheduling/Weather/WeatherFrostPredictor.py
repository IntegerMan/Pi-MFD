# coding=utf-8

"""
This file contains code related to getting frost predictions
"""
import datetime

from suds.client import Client

__author__ = 'Matt Eland'


class WeatherFrostPredictor(object):
    minutes_to_clean_frost = None

    def GetFrostPredictions(self):
        print('fetching frost data')
        client = Client("http://www.matteland.com/ANIServices/AniService.svc?wsdl")
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow_string = tomorrow.strftime('%Y-%m-%d')

        self.minutes_to_clean_frost = client.service.GetFrostScrapeTimeInMinutes(43035, tomorrow_string)