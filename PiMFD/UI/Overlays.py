# coding=utf-8

"""
Contains classes capable of performing various graphical overlay functions on the transparency layer
"""
from pygame.rect import Rect

from PiMFD.UI.Rendering import draw_horizontal_line, render_text, to_rgba, render_rectangle


__author__ = 'Matt Eland'


class Overlay(object):
    """
    An abstract class that contains common methods for overlays
    """

    def __init__(self, options):
        super(Overlay, self).__init__()
        self.options = options


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

        if not self.options.enable_scan_line:
            return

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


class InterlaceOverlay(Overlay):
    """
    Renders an alternating row interlace effect
    """

    alpha = 100

    def render(self, display, surface):
        """
        Renders an interlaced effect over everything
        :param display: The DisplayManager
        :param surface: The overlay graphical surface to render to
        """

        if not self.options.enable_interlacing:
            return

        color = (0, 0, 0, self.alpha)

        y = 1
        while y < display.res_y - 1:
            draw_horizontal_line(display, color, 0, display.res_x - 1, y, surface=surface)
            y += 2  # Move two lines down


class ShadowEffectOverlay(Overlay):
    """
    Renders an overlay simulating a shadow effect from the sides and top
    """

    alpha = 60
    size = 5

    def render(self, display, surface):
        """
        Renders an interlaced effect over everything
        :param display: The DisplayManager
        :param surface: The overlay graphical surface to render to
        """

        if not self.options.enable_shadow_effect:
            return

        color = (0, 0, 0, self.alpha)

        rect_top = Rect(0, 0, display.res_x, self.size)
        rect_left = Rect(0, self.size, self.size, display.res_y - self.size)
        rect_right = Rect(display.res_x - self.size, self.size, self.size, display.res_y - self.size)

        render_rectangle(display, color, rect_top, width=0, surface=surface)
        render_rectangle(display, color, rect_left, width=0, surface=surface)
        render_rectangle(display, color, rect_right, width=0, surface=surface)


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

        if not self.options.enable_fps:
            return

        fps = display.clock.get_fps()
        text = "{:.2f}".format(fps)
        color = display.color_scheme.highlight

        render_text(display, display.fonts.small, text, self.x, self.y, color, surface=surface)