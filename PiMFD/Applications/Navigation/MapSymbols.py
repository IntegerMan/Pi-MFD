# coding=utf-8

"""
Code organized around rendering locations to the map
"""
from PiMFD.Applications.Navigation.MapEntities import MapLocation
from PiMFD.UI.Rendering import render_text_centered

__author__ = 'Matt Eland'


class MapSymbol(MapLocation):
    """
    Renders a map symbol to the screen
    """

    def __init__(self, lat, lng, location):
        super(MapSymbol, self).__init__(lat, lng)

        self.tags = location.tags
        self.name = location.name

    def get_font_text_and_color(self, display):
        """
        Returns the font to use to display, the text to render, and the color to use
        :param display: The DisplayManager
        :return: the font to use to display, the text to render, and the color to use
        """
        return (display.fonts.small, self.name.upper(), display.color_scheme.highlight)

    def render(self, display):
        """
        Renders the symbol to the screen.
        :param display: The display manager
        """

        font, text, color = self.get_font_text_and_color(display)

        render_text_centered(display,
                             font,
                             text,
                             self.lat,
                             self.lng - (display.fonts.small.measure(text)[1] / 2.0),
                             color)


