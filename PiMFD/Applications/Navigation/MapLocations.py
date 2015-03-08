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
    
    id = None
    
    def __init__(self, controller, application, back_page):
        super(MapLocationAddPage, self).__init__(controller, application)

        self.btn_back = MFDButton("BACK")
        self.btn_add_location = MFDButton("ADD")
        self.back_page = back_page

        self.lbl_header = self.get_header_label('Add Location')

        self.txt_name = TextBox(self.display, self, label='Name:', text_width=300)
        self.txt_lat = TextBox(self.display, self, label=' Lat:', text_width=180)
        self.txt_lng = TextBox(self.display, self, label='Long:', text_width=180)
        self.txt_name.set_alphanumeric()
        self.txt_name.max_length = 20
        self.txt_lat.max_length = 12
        self.txt_lng.max_length = 12
        self.txt_lat.set_numeric(allow_decimal=True)
        self.txt_lng.set_numeric(allow_decimal=True)

        self.panel.children = [self.lbl_header, self.txt_name, self.txt_lat, self.txt_lng]

        self.data_provider = application.data_provider

        self.set_focus(self.txt_name)
        
    def set_values_from_context(self, context):
        
        if context:
            self.txt_lat.text = str(context.lat)
            self.txt_lng.text = str(context.lng)
            self.txt_name.text = context.get_display_name()
            self.id = context.id

    def get_lower_buttons(self):
        return [self.btn_back, self.btn_add_location]

    def handle_lower_button(self, index):

        if index == 0:  # Back
            self.application.select_page(self.back_page)
            return True

        elif index == 1:  # Add

            # Actually add the thing
            location = MapLocation(self.txt_name.text, self.txt_lat.text, self.txt_lng.text)
            location.id = self.id
            self.data_provider.add_location(location)

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


class MapLocationDetailsPage(MFDPage):

    def __init__(self, controller, application, location, back_page):
        super(MapLocationDetailsPage, self).__init__(controller, application)

        self.location = location

        self.btn_back = MFDButton("BACK")
        self.btn_save = MFDButton("SAVE")
        self.btn_home = MFDButton("HOME")
        self.btn_delete = MFDButton("DEL")
        self.back_page = back_page

        self.lbl_header = self.get_header_label('Edit Location')

        self.txt_name = TextBox(self.display, self, label='Name:', text_width=300, text=location.name)
        self.txt_lat = TextBox(self.display, self, label=' Lat:', text_width=180, text=location.lat)
        self.txt_lng = TextBox(self.display, self, label='Long:', text_width=180, text=location.lng)
        
        self.txt_name.set_alphanumeric()
        self.txt_name.max_length = 20
        self.txt_lat.max_length = 12
        self.txt_lng.max_length = 12
        self.txt_lat.set_numeric(allow_decimal=True)
        self.txt_lng.set_numeric(allow_decimal=True)

        self.panel.children = [self.lbl_header, self.txt_name, self.txt_lat, self.txt_lng]

        self.set_focus(self.txt_name)

    def get_lower_buttons(self):
        return [self.btn_back, self.btn_save, self.btn_home, None, self.btn_delete]

    def handle_lower_button(self, index):

        if index == 0:  # Back
            self.application.select_page(self.back_page)
            return True

        elif index == 1:  # Save

            # Actually add the thing
            self.location.name = self.txt_name.text
            self.location.lat = self.txt_lat.text
            self.location.lng = self.txt_lng.text
            self.application.data_provider.save_locations()

            self.application.select_page(self.back_page)
            return True

        elif index == 2:  # Home

            # Set this as home
            self.controller.options.lat = float(self.txt_lat.text)
            self.controller.options.lng = float(self.txt_lng.text)
            
            return True

        elif index == 4:  # Delete
            
            # TODO: Once my UI framework has grown a bit more, add a confirm functionality.
            self.application.delete_location(self.location)
            self.application.select_page(self.back_page)
            return True
        
        return super(MapLocationDetailsPage, self).handle_lower_button(index)

    def arrange(self):

        # Update the valid state of the add button
        if self.txt_lng.has_text() and self.txt_lat.has_text() and self.txt_name.has_text():
            self.btn_save.enabled = True
        else:
            self.btn_save.enabled = False
            
        # Mark as home if it's your home location
        try:
            if float(self.txt_lat.text) == self.controller.options.lat and \
               float(self.txt_lng.text) == self.controller.options.lng:
                self.btn_home.selected = True
            else:
                self.btn_home.selected = False
        except:
            self.btn_home.selected = False

        return super(MapLocationDetailsPage, self).arrange()

    def render(self):
        return super(MapLocationDetailsPage, self).render()
    

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
        self.data_provider = application.data_provider

        self.btn_back = MFDButton("BACK")
        self.btn_edit_location = MFDButton("EDIT")
        self.btn_add_location = MFDButton("NEW")
        self.back_page = back_page

    def handle_selected(self):

        is_first = True

        self.clear_focusables()
        if self.data_provider.locations and len(self.data_provider.locations) > 0:

            self.panel.children = [self.get_header_label('Locations ({})'.format(len(self.data_provider.locations)))]

            for l in self.data_provider.locations:

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
        return [self.btn_back, self.btn_edit_location, self.btn_add_location]

    def handle_lower_button(self, index):

        if index == 0:  # Back
            self.application.select_page(self.back_page)
            return True

        elif index == 1:  # Edit
            if self.focus:
                loc = self.focus.data_context
                if loc:
                    self.application.select_page(MapLocationDetailsPage(self.controller, self.application, loc, self))
                    return True

        elif index == 2:  # Add
            self.application.select_page(MapLocationAddPage(self.controller, self.application, self))
            return True

        return super(MapLocationsPage, self).handle_lower_button(index)

    def get_button_text(self):
        return "GOTO"

    def arrange(self):
        return super(MapLocationsPage, self).arrange()

    def render(self):

        if not self.data_provider.locations or len(self.data_provider.locations) < 0:
            self.center_text("NO LOCATIONS DEFINED")
        else:
            return super(MapLocationsPage, self).render()