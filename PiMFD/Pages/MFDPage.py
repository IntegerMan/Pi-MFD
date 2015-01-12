__author__ = 'Matt Eland'


class MFDPage(object):
    top_headers = list()
    bottom_headers = list()

    controller = None
    display = None

    def __init__(self, controller):
        self.controller = controller
        self.display = controller.display

    def get_button_text(self):
        return 'UNKN'

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


class MFDRootPage(MFDPage):
    def render(self, display):
        super(MFDRootPage, self).render(display)

        center_rect = display.render_text_centered(self.display.font_normal,
                                                   self.controller.app_name + ' ' + self.controller.app_version,
                                                   self.display.res_x / 2,
                                                   (self.display.res_y / 2) - (self.display.font_size_normal / 2),
                                                   self.display.color_scheme.highlight)

        display.render_text_centered(display.font_normal,
                                     'Systems Test',
                                     display.res_x / 2,
                                     center_rect.bottom + display.font_size_normal + display.padding_y,
                                     display.color_scheme.highlight)


class SimpleMessagePage(MFDPage):

    button_text = "NI"
    message = "Not Implemented"

    def __init__(self, controller, label, message='Not Implemented'):
        super(SimpleMessagePage, self).__init__(controller)
        self.button_text = label
        self.message = message

    def get_button_text(self):
        return self.button_text

    def render(self, display):
        super(SimpleMessagePage, self).render(display)

        display.render_text_centered(self.display.font_normal,
                                     self.message,
                                     self.display.res_x / 2,
                                     (self.display.res_y / 2) - (self.display.font_size_normal / 2),
                                     self.display.color_scheme.foreground)
