from time import strftime, gmtime
from TextUtilities import *
from PygameHelpers import *


__author__ = 'Matt Eland'

app_name = 'Pi-MFD'
app_version = '0.01 Development Version'


class ColorScheme(object):
    def __init__(self, background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255), selected=(255, 255, 255)):
        self.background = background
        self.foreground = foreground
        self.selected = selected
        self.highlight = highlight
        pass

    def clone_to(self, target):
        target.background = self.background
        target.foreground = self.foreground
        target.highlight = self.highlight
        target.selected = self.selected
        return target

    background = (0, 0, 0)
    foreground = (0, 255, 0)
    highlight = (255, 255, 255)
    selected = (255, 255, 255)

    pass


class ColorSchemes(object):
    # A green based color scheme resembling military avionics displays
    military = ColorScheme(background=(0, 8, 0), foreground=(0, 150, 0), selected=(0, 255, 0), highlight=(255, 255, 255))

    # A cyan display
    cyan = ColorScheme(background=(0, 0, 32), foreground=(0, 170, 170), selected=(0, 255, 255), highlight=(0, 0, 255))

    pass


class DisplaySettings(object):
    """Contains information related to the drawing dimensions of the application window as well as the drawing surface."""

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        pass

    def start_mfd(self):
        start_mfd(self)

    res_x = 800
    res_y = 480

    padding_x = 8
    padding_y = 8

    surface = None

    is_fullscreen = True

    frames_per_second = 30

    color_scheme = ColorSchemes.military

    font_size_normal = 24
    font_normal = None

    def get_content_start_y(self):
        return (self.padding_y * 2) + self.font_size_normal

    pass


class MFDController(object):

    display = None
    active_page = None
    continue_executing = True

    def __init__(self, display):
        self.display = display
        self.active_page = MFDRootPage(self)

    def process_events(self):
        # Process all events
        events = pygame.event.get()
        for event in events:

            # Check for Window Close
            if event.type == pygame.QUIT:
                self.continue_executing = False

            # Check for Keyboard Input
            if event.type == pygame.KEYDOWN:

                # Handle escape by closing the app.
                if event.key == pygame.K_ESCAPE:
                    self.continue_executing = False

    def update_application(self):

        page = self.active_page

        page.top_headers = list()
        page.top_headers.append(MFDButton("SCH", selected=True))
        page.top_headers.append(MFDButton("PRG"))
        page.top_headers.append(MFDButton("GAM"))
        page.top_headers.append(MFDButton("SOC"))
        page.top_headers.append(MFDButton("SYS"))

        page.bottom_headers = list()
        page.bottom_headers.append(MFDButton('TASK'))
        page.bottom_headers.append(MFDButton('MAIL'))
        page.bottom_headers.append(MFDButton('CAL'))
        page.bottom_headers.append(MFDButton('NAV'))
        page.bottom_headers.append(MFDButton('WTHR'))


class MFDButton(object):

    text = None
    enabled = True
    selected = False

    def __init__(self, text, selected=False, enabled=True):
        self.text = text
        self.selected = selected
        self.enabled = enabled

    def render(self, display, x, is_top):

        # Figure out where we're starting vertically
        y = display.padding_y
        if not is_top:
            y = display.res_y - display.padding_y - display.font_size_normal

        font_color = display.color_scheme.foreground

        label = self.text

        # If it's selected, use a different color and surround with brackets
        if self.selected:
            font_color = display.color_scheme.selected
            label = '[' + label + ']'

        pos = render_text(display, display.font_normal, label, x, y, font_color)

        line_length = 5

        if is_top:
            pygame.draw.line(display.surface, font_color, (x + (pos.width / 2), y - 2),
                             (x + (pos.width / 2), y - 2 - line_length))
        else:
            pygame.draw.line(display.surface, font_color, (x + (pos.width / 2), y + pos.height),
                             (x + (pos.width / 2), y + pos.height + line_length))


class MFDPage(object):

    top_headers = list()
    bottom_headers = list()

    controller = None
    display = None

    def __init__(self, controller):
        self.controller = controller
        self.display = controller.display

    def render_button_row(self, headers, is_top):

        start_x = self.display.padding_x
        end_x = self.display.res_x - self.display.padding_x

        num_headers = len(headers)
        if num_headers > 0:

            # Do division up front
            header_offset = (end_x - start_x) / num_headers
            half_offset = (header_offset / 2.0)

            # Render from left to right
            x_offset = 0
            for header in headers:
                x = start_x + x_offset + half_offset
                header.render(self.controller.display, x, is_top)
                x_offset += header_offset

    def render_button_rows(self):
        self.render_button_row(self.top_headers, True)
        self.render_button_row(self.bottom_headers, False)

    def render(self, display):

        # Render the headers
        self.render_button_rows()

        pass


class MFDRootPage(MFDPage):

    def render(self, display):
        super(MFDRootPage, self).render(display)

        center_rect = render_text_centered(self.display,
                                           self.display.font_normal,
                                           app_name + ' ' + app_version,
                                           self.display.res_x / 2,
                                           (self.display.res_y / 2) - (self.display.font_size_normal / 2),
                                           self.display.color_scheme.highlight)

        render_text_centered(self.display,
                             display.font_normal,
                             'Systems Test',
                             display.res_x / 2,
                             center_rect.top + display.font_size_normal + display.padding_y,
                             display.color_scheme.highlight)


class SysClockPage(MFDPage):

    def render(self, display):
        super(SysClockPage, self).render(display)

        x = display.padding_x
        y = display.get_content_start_y()

        time_format = '%m/%d/%Y - %H:%M:%S'

        # TODO: It should be simpler to render 3 lines of text

        rect = render_text(display,
                           display.font_normal,
                           "Current Time",
                           x,
                           y,
                           self.display.color_scheme.highlight)

        y = rect.bottom + display.padding_y

        rect = render_text(display,
                           display.font_normal,
                           strftime("SYS: " + time_format),
                           x,
                           y,
                           self.display.color_scheme.foreground)

        y = rect.bottom + display.padding_y

        render_text(display,
                    display.font_normal,
                    strftime("GMT: " + time_format, gmtime()),
                    x,
                    y,
                    display.color_scheme.foreground)


def start_mfd(display):

    # TODO: This should not need to know anything about pygame

    # Start up the graphics engine
    init_pygame_graphics(display, app_name)

    # Standard Timer
    clock = pygame.time.Clock()

    # Initialize the controller
    controller = MFDController(display)
    controller.active_page = SysClockPage(controller)

    # Main Processing Loop
    while controller.continue_executing:

        # Fill the background with black
        display.surface.fill(display.color_scheme.background)

        # Update the headers
        controller.update_application()

        # Render the current page
        controller.active_page.render(display)

        # Handle input, allow user to close window / exit / control the app
        controller.process_events()

        # Update the UI and give a bit of time before going again
        pygame.display.update()
        clock.tick(display.frames_per_second)
