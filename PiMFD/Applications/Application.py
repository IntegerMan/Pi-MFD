__author__ = 'Matt Eland'


class MFDApplication(object):

    controller = None
    display = None

    def __init__(self, controller):
        self.controller = controller
        self.display = controller.display

    def get_buttons(self):
        # Sub-classes will return a real implementation. By default, go with an empty list.
        return list()

    def get_default_page(self):
        return None

    def get_button_text(self):
        return 'UNKN'

class PlaceholderApp(MFDApplication):

    button_text = 'UNKN'

    def __init__(self, controller, label):
        super(PlaceholderApp, self).__init__(controller)
        self.button_text = label

    def get_button_text(self):
        return self.button_text