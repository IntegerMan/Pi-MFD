# coding=utf-8
"""
Contains core application definition and placeholders.
"""
from PiMFD.Button import MFDButton

__author__ = 'Matt Eland'


class MFDApplication(object):
    """
    An abstract class representing the base of all applications.
    :type controller: PiMFD.Controller.MFDController The controller
    """
    pages = None

    active_page = None
    controller = None
    display = None

    def __init__(self, controller):
        self.controller = controller
        self.display = controller.display
        self.pages = list()

    def get_buttons(self):
        """
        Gets the page buttons associated with the application.
        :return: the page buttons associated with the application.
        """
        buttons = list()
        for page in self.pages[0:self.controller.max_page_buttons]:  # TODO: Support paging for > max_page_buttons pages
            buttons.append(MFDButton(page.get_button_text(), selected=(self.active_page is page)))

        return buttons

    def get_default_page(self):
        """
        Gets the default page.
        :return: The default page.
        """
        return None

    def get_button_text(self):
        """
        Gets the text used to render the button
        :return: the text used to render the button
        """
        return 'UNKN'

    def handle_unselected(self):
        """
        Occurs when the application is unselected (as another app is being selected)
        """
        self.select_page(None)

    def handle_selected(self):
        """
        Occurs when the application is being selected
        """
        self.select_page(self.get_default_page())

    def handle_reselected(self):
        """
        Occurs when the user selects the application while the application is already selected. This is useful in
        some cases for special button handling.
        """
        self.select_page(self.get_default_page())

    # noinspection PyMethodMayBeStatic
    def page_reselected(self, page):
        """
        Occurs when a page in this application is reselected (selected while already selected)
        :type page: MFDPage The page being reselected
        """
        pass

    def select_page_by_index(self, index):
        """
        Selects the specified page in the application by its 0-based index
        :type index: int The 0-based index of the page we selected.
        """

        # Figure out what we clicked
        if index < len(self.pages):
            page = self.pages[index]
        else:
            page = None

        self.select_page(page)

    def select_page(self, page):
        """
        Selects the specified page
        :type page: The MFDPage in this application
        """

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


class PlaceholderApp(MFDApplication):

    """
    A placeholder application representing content not implemented yet. Built for easier prototyping.
    :type controller: PiMFD.Controller.MFDController T he controller
    :type label: str The button label for the application.
    """
    button_text = 'UNKN'

    def __init__(self, controller, label):
        super(PlaceholderApp, self).__init__(controller)
        self.button_text = label

    def get_button_text(self):
        """
        Gets the text used to render the button
        :return: the text used to render the button
        """
        return self.button_text