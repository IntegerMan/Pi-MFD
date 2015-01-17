# coding=utf-8

"""
Contains classes capable of performing various graphical overlay functions on the transparency layer
"""
from PiMFD.UI.Rendering import draw_horizontal_line, render_text, to_rgba

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
            alpha = (i * self.intensity)
            draw_horizontal_line(display, to_rgba(c, alpha), 0, max_x, self.y + i, surface=surface)

        # Animate downwards - try to keep a constant perceived pace, regardless of FPS setting
        effective_speed = self.speed * (60.0 / display.frames_per_second)
        if self.y < display.res_y + self.height + (self.delay * effective_speed):
            self.y += effective_speed
        else:
            self.y = -self.height


class FPSOverlay(Overlay):
    """
    Renders Frames Per Second to the Screen
    """

    y = 14
    x = 4

    def render(self, display, surface):
        """
        Renders the overlay
        :param display: The DisplayManager
        :param surface: The overlay graphical surface to render to
        """

        fps = display.clock.get_fps()
        text = "{:.2f}".format(fps)
        color = display.color_scheme.highlight

        render_text(display, display.font_small, text, self.x, self.y, color, surface=surface)