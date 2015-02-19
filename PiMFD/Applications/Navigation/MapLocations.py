# coding=utf-8

"""
This file contains map locations information
"""

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Button import MFDButton
from PiMFD.UI.TextBoxes import TextBox
from PiMFD.UI.Widgets.MenuItem import TextMenuItem

__author__ = 'Matt Eland'


class MapLocation(object):
    """
    Represents a location on the map
    :param name: The name of the location 
    :type name: basestring
    :param lat: The latitude
    :type lat: float
    :param lng: The longitude
    :type lng: float
    """
    name = None
    lat = None
    lng = None
    tags = {}
    id = None

    def __init__(self, name, lat, lng):
        super(MapLocation, self).__init__()

        self.name = name
        self.lat = lat
        self.lng = lng


class MapLocationAddPage(MFDPage):
    
    def __init__(self, controller, application, map_context, back_page):
        super(MapLocationAddPage, self).__init__(controller, application)
        self.map_context = map_context

        self.btn_back = MFDButton("BACK")
        self.btn_add_location = MFDButton("ADD")
        self.back_page = back_page

        self.lbl_header = self.get_header_label('Add Location')

        self.txt_name = TextBox(self.display, self, label='Name:', text_width=300)
        self.txt_lat = TextBox(self.display, self, label=' Lat:', text_width=160)
        self.txt_lng = TextBox(self.display, self, label='Long:', text_width=160)
        self.txt_name.set_alphanumeric()
        self.txt_name.max_length = 20
        self.txt_lat.max_length = 10
        self.txt_lng.max_length = 10
        self.txt_lat.set_numeric(allow_decimal=True)
        self.txt_lng.set_numeric(allow_decimal=True)

        self.panel.children = [self.lbl_header, self.txt_name, self.txt_lat, self.txt_lng]

        self.set_focus(self.txt_name)

    def get_lower_buttons(self):
        return [self.btn_back, self.btn_add_location]

    def handle_lower_button(self, index):

        if index == 0:  # Back
            self.application.select_page(self.back_page)
            return True

        elif index == 1:  # Add

            # Actually add the thing
            location = MapLocation(self.txt_name.text, self.txt_lat.text, self.txt_lng.text)
            self.application.add_location(location)

            self.application.select_page(self.back_page)
            return True

        return super(MapLocationAddPage, self).handle_lower_button(index)

    def arrange(self):

        # Update the valid state of the add button
        if self.txt_lng.has_text() and self.txt_lat.has_text() and self.txt_name.has_text():
            self.btn_add_location.enabled = True
        else:
            self.btn_add_location.enabled = False

        return super(MapLocationAddPage, self).arrange()

    def render(self):
        return super(MapLocationAddPage, self).render()


class MapLocationsPage(MFDPage):
    """
    Lists map locations the user has saved
    :param controller: The controller
    :param application: The navigation application
    :param map_context: The map context
    """

    def __init__(self, controller, application, map_context, back_page):
        super(MapLocationsPage, self).__init__(controller, application)
        self.map_context = map_context

        self.btn_back = MFDButton("BACK")
        self.btn_add_location = MFDButton("NEW")
        self.back_page = back_page

    def handle_selected(self):

        is_first = True

        if self.application.locations and len(self.application.locations) > 0:

            self.panel.children = [self.get_header_label('Locations ({})'.format(len(self.application.locations)))]

            for l in self.application.locations:

                item = TextMenuItem(self.display, self, '{}: {}, {}'.format(l.name, l.lat, l.lng))
                item.font = self.display.fonts.list
                item.data_context = l
                self.panel.children.append(item)

                if is_first:
                    self.set_focus(item)
                    is_first = False

        super(MapLocationsPage, self).handle_selected()

    def handle_control_state_changed(self, widget):
        
        location = widget.data_context
        if location:
            self.application.show_map(location.lat, location.lng)

        super(MapLocationsPage, self).handle_control_state_changed(widget)

    def get_lower_buttons(self):
        return [self.btn_back, self.btn_add_location]

    def handle_lower_button(self, index):

        if index == 0:  # Back
            self.application.select_page(self.back_page)
            return True

        elif index == 1:  # Add
            self.application.select_page(MapLocationAddPage(self.controller, self.application, self.map_context, self))
            return True

        return super(MapLocationsPage, self).handle_lower_button(index)

    def get_button_text(self):
        return "GOTO"

    def arrange(self):
        return super(MapLocationsPage, self).arrange()

    def render(self):

        if not self.application.locations or len(self.application.locations) < 0:
            self.center_text("NO LOCATIONS DEFINED")
        else:
            return super(MapLocationsPage, self).render()