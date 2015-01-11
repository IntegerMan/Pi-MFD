from PiMFD.Applications.Application import MFDApplication
from PiMFD.Button import MFDButton

__author__ = 'Matt Eland'


class SysApplication(MFDApplication):


    def get_buttons(self):
        buttons = list()
        buttons.append(MFDButton('TIME', selected=True))
        buttons.append(MFDButton('PERF'))
        buttons.append(MFDButton('NET'))
        buttons.append(MFDButton('OPTS'))
        buttons.append(MFDButton('EXIT'))
        return buttons

