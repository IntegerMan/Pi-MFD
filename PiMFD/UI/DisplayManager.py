# coding=utf-8
"""
The primary display control module responsible for arranging and rendering components on the display and acting as a
liaison between the application and Pygame.
"""
import pygame

from PiMFD import start_mfd
from PiMFD.UI.ColorScheme import ColorSchemes
from PiMFD.UI.Rendering import draw_horizontal_line


__author__ = 'Matt Eland'


class DisplayManager(object):
    """
    Contains information and functions related to the drawing dimensions of the application window as well as
    the drawing surface.
    """

    res_x = 800
    res_y = 480

    clock = None

    padding_x = 16
    padding_y = 8

    overlays = None

    surface = None
    overlay_surface = None

    is_fullscreen = False

    frames_per_second = 60

    color_scheme = ColorSchemes.get_green_color_scheme()

    font_size_normal = 24
    font_normal = None

    font_size_small = 12
    font_small = None

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        self.overlays = list()

    def start_mfd(self, app_options):
        """
        Starts the MFD Application
        :type app_options: PiMFD.MFDAppOptions the app options
        """
        start_mfd(self, app_options)

    def update_graphics_mode(self):
        """
        Causes the graphics mode to refresh to take into account new resolutions
        """
        pygame.display.update()
        self.overlay_surface = pygame.Surface((self.res_x, self.res_y), pygame.SRCALPHA)
        self.overlay_surface.convert_alpha()

    def wait_for_next_frame(self):
        """
        Updates the display and waits until it's time to render the next frame (prevent us from going too fast)
        """
        pygame.display.update()
        self.clock.tick(self.frames_per_second)

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
                draw_horizontal_line(self, self.color_scheme.interlace_color, 0, self.res_x - 1, y)
                y += 2  # Move two lines down

    def render_overlays(self):
        """
        Renders overlays on top of the application's normal graphics layer
        """

        # Start fully transparent
        self.overlay_surface.fill((0, 0, 0, 0))

        # Render all overlays onto the surface
        for overlay in self.overlays:
            overlay.render(self, self.overlay_surface)

        # Pass the contents on to the primary surface
        self.surface.blit(self.overlay_surface, (0, 0))

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

    def render_text(self, font, text, left, top, color, background=None, surface=None):
        """
        Renders text to the screen at the specified coordinates with the specified display parameters
        :type font: pygame.ftfont.Font The font used to render the text
        :type text: str The text to render
        :type left: int The x coordinate for the left edge of the text block
        :type top: int The y coordinate for the top edge of the text block
        :type color: tuple The RGB color to render the text using
        :type background: unknown or tuple The RGB color to render the background or None (default) for transparent
        :param surface: The surface to render to. Defaults to the primary surface.
        :return: A Rect representing the rendered area for the text
        """
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(top=top, left=left)

        if surface is None:
            surface = self.surface

        if background:
            surface.fill(background, rect=rect)

        surface.blit(text_surface, rect)
        return rect

    def render_text_centered(self, font, text, left, top, color, background=None, surface=None):
        """
        Renders text centered horizontally around the specified points
        :type font: pygame.ftfont.Font The font used to render the text
        :type text: str The text to render
        :type left: int The x coordinate for the center of the text block
        :type top: int The y coordinate for the top of the text block
        :type color: tuple The RGB color to render the text using
        :type background: unknown or tuple The RGB color to render the background or None (default) for transparent
        :param surface: The surface to render to. Defaults to the primary surface.
        :return: A Rect representing the rendered area for the text
        """
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(left, top + (font.size(text)[1] / 2)))

        if surface is None:
            surface = self.surface

        if background:
            surface.fill(background, rect=rect)

        surface.blit(text_surface, rect)
        return rect

    @staticmethod
    def to_rgba(color, alpha=255):
        """
        Takes a RGB color tuple and adds an alpha value to it
        :param color: The RGB color
        :param alpha: The alpha value (0-255)
        :return: A RGBA color structure
        """
        return color[0], color[1], color[2], alpha

    def init_graphics(self, title, font_name):
        """
        Initializes graphics via pygame.
        :param title: The title of the application
        :param font_name: The font to use for the primary application font
        """

        # Initialize the pygame engine
        pygame.init()
        self.clock = pygame.time.Clock()

        # If we haven't configured width / height, grab them from the current resolution
        if self.res_x is None or self.res_x < 8 or self.res_y is None or self.res_y < 8:
            self.grab_dimensions_from_current_resolution()

        # Prepare the Display
        if self.is_fullscreen:
            display = pygame.display.set_mode((self.res_x, self.res_y), pygame.FULLSCREEN)
        else:
            display = pygame.display.set_mode((self.res_x, self.res_y), pygame.RESIZABLE)

        # Customize the Window
        pygame.display.set_caption(title)

        # Set up Fonts
        self.font_small = pygame.font.Font(font_name, self.font_size_small)
        self.font_normal = pygame.font.Font(font_name, self.font_size_normal)

        # Time to use our output
        self.surface = display
        self.surface.convert()
        self.overlay_surface = pygame.Surface((self.res_x, self.res_y), pygame.SRCALPHA)
        self.overlay_surface.convert_alpha()

    def grab_dimensions_from_current_resolution(self):
        """
        Sets the dimensions of this object based on the current screen's resolution.
        """
        info = pygame.display.Info()
        self.res_x = info.current_w
        self.res_y = info.current_h
