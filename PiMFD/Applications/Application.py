from PiMFD.Button import MFDButton

__author__ = 'Matt Eland'


class MFDApplication(object):

    pages = list()

    controller = None
    display = None

    def __init__(self, controller):
        self.controller = controller
        self.display = controller.display

    def get_buttons(self):
        buttons = list()
        for page in self.pages:
            buttons.append(MFDButton(page.get_button_text(), selected=(self.active_page is page)))

        return buttons

    def get_default_page(self):
        return None

    def get_button_text(self):
        return 'UNKN'

    def handle_unselected(self):
        self.active_page = None

    def handle_selected(self):
        self.active_page = self.get_default_page()

    def handle_reselected(self):
        pass

    def select_page(self, index):

        # Figure out what we clicked
        page = self.pages[index]

        # Don't allow switching to a "none" page
        if page is None:
            return

        if page is self.active_page:

            # Some pages will want to handle getting reselected as a special event
            page.handle_reselected()

        else:

            # Tell the other page it's getting deselected
            if self.active_page is not None:
                self.active_page.handle_unselected()

            # Update the current page to the new page and tell it that it's been selected
            self.active_page = page
            page.handle_selected()

        pass


class PlaceholderApp(MFDApplication):

    button_text = 'UNKN'

    def __init__(self, controller, label):
        super(PlaceholderApp, self).__init__(controller)
        self.button_text = label

    def get_button_text(self):
        return self.button_text