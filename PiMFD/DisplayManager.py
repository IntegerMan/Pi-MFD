# coding=utf-8
"""
The primary display control module responsible for arranging and rendering components on the display and acting as a
liaison between the application and Pygame.
"""
import pygame

from PiMFD import start_mfd
from PiMFD.ColorScheme import ColorSchemes


__author__ = 'Matt Eland'


class DisplayManager(object):
    """
    Contains information and functions related to the drawing dimensions of the application window as well as
    the drawing surface.
    """

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        pass

    def start_mfd(self, app_options):
        """
        Starts the MFD Application
        :type app_options: PiMFD.MFDAppOptions the app options
        """
        start_mfd(self, app_options)

    res_x = 800
    res_y = 480

    padding_x = 16
    padding_y = 8

    surface = None

    is_fullscreen = False

    frames_per_second = 30

    color_scheme = ColorSchemes.get_green_color_scheme()

    font_size_normal = 24
    font_normal = None

    def render_background(self):
        """
        Renders the application background
        """

        # Fill the background with a solid color
        self.surface.fill(self.color_scheme.background)

        # If we're using an interlace color, render it on every other line
        if self.color_scheme.interlace_color is not None:
            y = 1
            while y < self.res_y - 1:
                self.draw_horizontal_line(self.color_scheme.interlace_color, 0, self.res_x - 1, y)
                y += 2  # Move two lines down

    def draw_horizontal_line(self, color, x1, x2, y):
        """
        Renders a horizontal line along a single vertical plane
        :type color: The RGB value to render
        :type x1: int the starting X coordinate of the line
        :type x2: int the ending X coordinate of the line
        :type y: int the Y coordinate for both ends of the line
        """
        pygame.draw.line(self.surface, color, (x1, y), (x2, y))

    def draw_vertical_line(self, color, x, y1, y2):
        """
        Renders a vertical line along a single horizontal plane
        :type color: The RGB value to render
        :type x: int the X coordinate for both ends of the line
        :type y1: int the starting X coordinate of the line
        :type y2: int the ending X coordinate of the line
        """
        pygame.draw.line(self.surface, color, (x, y1), (x, y2))

    def draw_rectangle(self, color, rect, width=1):
        """
        Draws a rectangle
        :param color: The color to use to draw
        :param rect: The bounds of the rectangle
        :param width: The width of the rectangle. If 0, this will be a solid fill. Defaults to 1.
        """
        pygame.draw.rect(self.surface, color, rect, width)

    def get_content_start_x(self):
        """
        Gets the X indentation level for content
        :return: The X location at which content rendering is acceptable
        """
        return self.padding_x * 2

    def get_content_start_y(self):
        """
        Gets the Y indentation level for content
        :return: The Y location at which content rendering is acceptable
        """
        return (self.padding_y * 4) + self.font_size_normal

    def get_spacer_line_height(self, font_size=None):
        """
        Calculates the Y amount of padding needed for a single blank line
        :type font_size: int The size of the font or None to use the height from font_size_normal
        :return:
        """
        if font_size is None:
            font_size = self.font_size_normal

        return (self.padding_y * 2) + font_size

    def render_text(self, font, text, left, top, color, background=None):
        """
        Renders text to the screen at the specified coordinates with the specified display parameters
        :type font: pygame.ftfont.Font The font used to render the text
        :type text: str The text to render
        :type left: int The x coordinate for the left edge of the text block
        :type top: int The y coordinate for the top edge of the text block
        :type color: tuple The RGB color to render the text using
        :type background: unknown or tuple The RGB color to render the background or None (default) for transparent
        :return: A Rect representing the rendered area for the text
        """
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(top=top, left=left)

        if background:
            self.surface.fill(background, rect=rect)

        self.surface.blit(text_surface, rect)
        return rect

    def render_text_centered(self, font, text, left, top, color, background=None):
        """
        Renders text centered horizontally around the specified points
        :type font: pygame.ftfont.Font The font used to render the text
        :type text: str The text to render
        :type left: int The x coordinate for the center of the text block
        :type top: int The y coordinate for the top of the text block
        :type color: tuple The RGB color to render the text using
        :type background: unknown or tuple The RGB color to render the background or None (default) for transparent
        :return: A Rect representing the rendered area for the text
        """
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(left, top + (font.size(text)[1] / 2)))

        if background:
            self.surface.fill(background, rect=rect)

        self.surface.blit(text_surface, rect)
        return rect

    def init_graphics(self, title, font_name):
        """
        Initializes graphics via pygame.
        :param title: The title of the application
        :param font_name: The font to use for the primary application font
        """
        pygame.init()

        # If we haven't configured width / height, grab them from the current resolution
        if self.res_x is None or self.res_x < 8 or self.res_y is None or self.res_y < 8:
            self.grab_dimensions_from_current_resolution()

        # Prepare the Display
        if self.is_fullscreen:
            display = pygame.display.set_mode((self.res_x, self.res_y), pygame.FULLSCREEN)
        else:
            display = pygame.display.set_mode((self.res_x, self.res_y), pygame.RESIZABLE)

        # Don't settle with that silly "pygame window" label
        pygame.display.set_caption(title)

        # Time to use our output
        self.font_normal = pygame.font.Font(font_name, self.font_size_normal)
        self.surface = display

    def grab_dimensions_from_current_resolution(self):
        """
        Sets the dimensions of this object based on the current screen's resolution.
        """
        info = pygame.display.Info()
        self.res_x = info.current_w
        self.res_y = info.current_h
