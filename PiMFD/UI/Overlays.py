# coding=utf-8

"""
Contains classes capable of performing various graphical overlay functions on the transparency layer
"""

__author__ = 'Matt Eland'


class Overlay(object):
    """
    An abstract class that contains common methods for overlays
    """

    def render(self, display, surface):
        """
        Renders the overlay
        :param display: The DisplayManager
        :param surface: The overlay graphical surface to render to
        """
        pass


class ScanlineOverlay(Overlay):
    """
    A procedural scanline overlay that renders an animated scanline over the application window
    """

    y = 0
    speed = 3
    height = 20
    intensity = 1.25
    delay = 240

    def render(self, display, surface):
        """
        Renders the overlay
        :param display: The DisplayManager
        :param surface: The overlay graphical surface to render to
        """

        max_x = display.res_x - 1

        # Draw our line
        c = display.color_scheme.highlight
        for i in range(0, self.height):
            display.draw_horizontal_line((c[0], c[1], c[2], (i * self.intensity)), 0, max_x, self.y + i,
                                         surface=surface)

        # Advance to the next row
        if self.y < display.res_y + self.height + (self.delay * self.speed):
            self.y += self.speed
        else:
            self.y = -self.height