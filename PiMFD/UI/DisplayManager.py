# coding=utf-8
"""
Contains DisplayManager.
"""
import pygame

from PiMFD import start_mfd
from PiMFD.UI.ColorScheme import ColorSchemes
from PiMFD.UI.Fonts import FontManager
from PiMFD.UI.Overlays import ScanlineOverlay, InterlaceOverlay, FPSOverlay, ShadowEffectOverlay


__author__ = 'Matt Eland'


class DisplayManager(object):
    """
    Handles surface management, resolution, frames per second, and overall coordination of the graphical engine.
    Individual rendering methods are now found in Rendering.py
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
    allow_resize = True

    frames_per_second = 60

    color_scheme = None
    color_schemes = []

    fonts = None

    options = None

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        self.overlays = list()
        self.color_schemes = ColorSchemes.get_color_schemes()
        self.color_scheme = self.color_schemes[0]

    def start_mfd(self, app_options):
        """
        Starts the MFD Application
        :type app_options: PiMFD.MFDAppOptions the app options
        """
        self.options = app_options
        start_mfd(self, app_options)

    def update_graphics_mode(self):
        """
        Causes the graphics mode to refresh to take into account new resolutions
        """
        pygame.display.update()
        self.overlay_surface = pygame.Surface((self.res_x, self.res_y), pygame.SRCALPHA)
        self.overlay_surface.convert_alpha()

    def set_fullscreen(self, is_fullscreen):
        """
        :type is_fullscreen: bool
        """
        self.is_fullscreen = is_fullscreen
        self.prepare_display_surface()

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

    def get_content_end_x(self):
        """
        Gets the right X indentation level for content
        :return: The X location at which content rendering is no longer acceptable
        """
        return self.res_x - (self.padding_x * 2)

    def get_content_start_y(self):
        """
        Gets the Y indentation level for content
        :return: The Y location at which content rendering is acceptable
        """
        return (self.padding_y * 4) + self.fonts.normal.size

    def get_content_end_y(self):
        """
        Gets the bottom Y indentation level for content
        :return: The Y location at which content rendering is no longer acceptable
        """
        return self.res_y - ((self.padding_y * 4) + self.fonts.normal.size)

    def get_content_start_pos(self):
        """
        Gets positional coordinates for X and Y start for content
        :return: positional coordinates for X and Y start
        """
        return self.get_content_start_x(), self.get_content_start_y()

    def get_spacer_line_height(self, font_size=None):
        """
        Calculates the Y amount of padding needed for a single blank line
        :type font_size: int The size of the font or None to use the height from font_size_normal
        :return:
        """
        if font_size is None:
            font_size = self.fonts.normal.size

        return (self.padding_y * 2) + font_size

    def prepare_display_surface(self):

        # Quit / Init can help window transitions
        pygame.display.quit()
        pygame.display.init()

        res = (self.res_x, self.res_y)

        # Prepare the Display
        if self.is_fullscreen:
            print('setting to fullscreen {}, {}'.format(res[0], res[1]))
            display = pygame.display.set_mode(res, pygame.FULLSCREEN)
        elif self.allow_resize:
            print('setting to resizable window {}, {}'.format(res[0], res[1]))
            display = pygame.display.set_mode(res, pygame.RESIZABLE)
        else:
            print('setting to window {}, {}'.format(res[0], res[1]))
            display = pygame.display.set_mode(res, 0)

        # Customize the Window
        pygame.display.set_caption(self.options.app_name)

        # Time to use our output
        self.surface = display
        self.surface.convert()
        self.overlay_surface = pygame.Surface(res, pygame.SRCALPHA)
        self.overlay_surface.convert_alpha()

        pygame.display.update()

    def init_graphics(self, options):
        """
        Initializes graphics via pygame.
        :param options: The application options
        """

        # Grab color scheme if we can and use that
        if options.color_scheme and options.color_scheme != self.color_scheme.name:
            for cs in self.color_schemes:
                if cs.name == options.color_scheme:
                    self.color_scheme = cs
                    break

        # Initialize the pygame engine
        pygame.init()
        
        # Initialize Joystick Input
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for stick in joysticks:
            stick.init()
            
        self.clock = pygame.time.Clock()

        # If we haven't configured width / height, grab them from the current resolution
        if self.res_x is None or self.res_x < 8 or self.res_y is None or self.res_y < 8:
            set_resolution = True
        else:
            set_resolution = False

        self.grab_dimensions_from_current_resolution(set_resolution=set_resolution)

        # Initialize the display resolution
        self.prepare_display_surface()

        # Set up Fonts
        self.fonts = FontManager(options)
        self.fonts.load_fonts()

        # Initialize our overlays
        self.init_overlays(options)

    def grab_dimensions_from_current_resolution(self, set_resolution=True):
        """
        Sets the dimensions of this object based on the current screen's resolution.
        """
        info = pygame.display.Info()

        self.desktop_x, self.desktop_y = info.current_w, info.current_h

        if set_resolution:
            self.res_x = info.current_w
            self.res_y = info.current_h

    def init_overlays(self, options):
        """
        Initializes the overlays layer
        :type options: PiMFD.Options.MFDAppOptions
        """
        self.overlays.append(ShadowEffectOverlay(options))
        self.overlays.append(ScanlineOverlay(options))
        self.overlays.append(InterlaceOverlay(options))
        self.overlays.append(FPSOverlay(options))

    def get_content_size(self):

        """
        Gets the width and height of the content area
        :rtype : tuple
        :return: The width and height of the content area
        """

        width = self.get_content_end_x() - self.get_content_start_x()
        height = self.get_content_end_y() - self.get_content_start_y()

        return width, height
