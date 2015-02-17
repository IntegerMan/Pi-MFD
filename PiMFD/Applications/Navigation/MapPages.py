# coding=utf-8

"""
This file will hold map pages
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.Applications.Navigation.MapRendering import MapRenderer
from PiMFD.UI import Keycodes
from PiMFD.UI.Keycodes import is_up_key, is_right_key, is_left_key, is_down_key, is_enter_key
from PiMFD.UI.Panels import StackPanel

__author__ = 'Matt Eland'


class MapPage(MFDPage):

    lbl_loading = None
    map_renderer = None
    context = None

    def __init__(self, controller, application):
        super(MapPage, self).__init__(controller, application)

        self.map_renderer = MapRenderer(application.map, controller.display, application.map_context)
        self.context = application.map_context

    def get_button_text(self):
        return self.application.map_context.active_filter.get_button_text()

    def render(self):

        if self.application.map.has_data:
            self.map_renderer.render()
        else:
            self.center_text(self.context.map.status_text.upper())

        return super(MapPage, self).render()

    def handle_reselected(self):
        self.application.next_map_mode()
        super(MapPage, self).handle_reselected()

    def handle_mouse_left_click(self, pos):

        if self.context.page_mode == 'CUR':
            self.context.cursor_pos = pos
            self.controller.play_button_sound()
            return True

        return super(MapPage, self).handle_mouse_left_click(pos)

    def handle_key(self, key):

        if key == Keycodes.KEY_KP_PLUS or key == Keycodes.KEY_PLUS or key == Keycodes.KEY_PAGEUP:
            self.application.zoom_in()
            return True

        elif key == Keycodes.KEY_KP_MINUS or key == Keycodes.KEY_MINUS or key == Keycodes.KEY_PAGEDOWN:
            self.application.zoom_out()
            return True

        elif is_up_key(key):
            self.context.move_up()
            return True

        elif is_right_key(key):
            self.context.move_right()
            return True

        elif is_down_key(key):
            self.context.move_down()
            return True

        elif is_left_key(key):
            self.context.move_left()
            return True

        elif is_enter_key(key):
            if self.application.btn_info.enabled:
                self.application.select_page_by_index(2)
                return True

        elif key in (Keycodes.KEY_KP0, Keycodes.KEY_KP_MULTIPLY, Keycodes.KEY_KP_DIVIDE):
            self.application.select_page_by_index(1)

        elif key == Keycodes.KEY_KP5:
            self.application.get_map_data_on_current_cursor_pos()

        return super(MapPage, self).handle_key(key)

class MapInfoPage(MFDPage):

    lbl_header = None
    map_context = None
    image = None
    is_fullscreen_image = False

    def __init__(self, controller, application):
        super(MapInfoPage, self).__init__(controller, application)

        self.map_context = application.map_context
        self.lbl_header = self.get_header_label('{}')
        self.lbl_pos = self.get_label("GPS: {}, {}")
        self.pnl_tags = StackPanel(controller.display, self)
        self.pnl_image = StackPanel(controller.display, self)
        self.pnl_horizontal = StackPanel(controller.display, self, is_horizontal=True)
        self.pnl_horizontal.children = [self.pnl_image, self.pnl_tags]
        self.panel.children = [self.lbl_header, self.lbl_pos, self.pnl_horizontal]

    def render(self):

        if self.image:
            if self.is_fullscreen_image:

                # Maximize the image!
                self.image.min_width = self.display.bounds.right
                self.image.max_width = self.image.min_width

                # All we want to render is the image, so just do it now. This will preclude normal data rendering
                return self.image.render_at((0, 0))

            else:

                # Reset the funkiness caused by full-screening an image
                self.image.max_width = self.display.bounds.right - 400
                self.image.min_width = None

        return super(MapInfoPage, self).render()

    def get_button_text(self):
        return "INFO"

    def get_image_url(self, context):

        if 'contact:webcam' in context.tags:
            return context.tags['contact:webcam']
        elif 'image' in context.tags:
            return context.tags['image']

        return None

    def handle_selected(self):

        context = self.map_context.cursor_context

        name = context.get_display_name(abbreviate=False)
        if name:
            self.lbl_header.text_data = name
        else:
            self.lbl_header.text_data = 'Node Info'

        self.lbl_pos.text_data = context.lat, context.lng

        # By default, clear out our image settings
        self.pnl_image.children = []
        self.image = None

        # If we support images, show an image
        image_url = self.get_image_url(context)
        if image_url:

            # Determine Refresh Interval
            if 'interval' in context.tags:
                interval = context.tags['interval']
            else:
                interval = 0

            # Build an image control
            max_width = self.display.bounds.right - 400
            if max_width > 8:
                self.image = self.get_image(image_url, interval=interval, max_width=max_width)
                if self.image:
                    # Tell the page it has image content (will be used for selective rendering)
                    self.pnl_image.children = [self.image]

        # Build a list of labels for all tags in this shape
        tags = []
        for key in context.tags:
            tag = (key, context.tags[key])

            if self.should_show_tag(tag, context):
                tag_string = self.get_tag_string(tag, context)
                tag_label = self.get_label(tag_string)
                tags.append(tag_label)

        # Set the labels into the children collection
        self.pnl_tags.children = tags

        # Start Surveillance Cameras in Fullscreen mode; ensure others start normal mode.
        if self.image and ('surveillance' in context.tags or 'contact:webcam' in context.tags):
            self.is_fullscreen_image = True
        else:
            self.is_fullscreen_image = False

        # Determine if an action is possible and, if so, enable the details button
        if self.image or self.is_fullscreen_image:
            self.application.btn_detail_action.enabled = True
        else:
            self.application.btn_detail_action.enabled = False

        if self.is_fullscreen_image:
            self.application.btn_detail_action.text = "INFO"
        else:
            self.application.btn_detail_action.text = "DTLS"

        super(MapInfoPage, self).handle_selected()

    def toggle_details(self):
        if self.image and not self.is_fullscreen_image:
            self.is_fullscreen_image = True
            self.application.btn_detail_action.text = "INFO"
        else:
            self.is_fullscreen_image = False
            self.application.btn_detail_action.text = "DTLS"

    def get_tag_string(self, tag, entity):

        handler = self.map_context.tag_handlers.get_handler(tag[0])
        if handler:
            text = handler.get_description_text(entity, tag[1])
            if text:
                return text

        if tag[0] == 'ele':
            return 'Elevation: {}'.format(tag[1])

        if tag[0] == 'traffic_sign':
            if tag[1] == 'yes':
                return 'Traffic Sign'
            else:
                return 'Traffic Sign: {}'.format(tag[1])

        if tag[0] == 'water':
            if tag[1] == 'pond':
                return 'Pond'

        if tag[0] == 'bridge':
            if tag[1] == 'yes':
                return 'Bridge'

        if tag[0] == 'access':
            if tag[1] == 'public':
                return 'Public Access'
            elif tag[1] == 'permissive':
                return 'Open to Public'
            elif tag[1] == 'private':
                return 'Private Access'
            elif tag[1] == 'no':
                return 'No Access'
            elif tag[1] == 'destination':
                return 'Local Access Only'
            elif tag[1] == 'discouraged':
                return 'Access Discouraged'
            elif tag[1] == 'designated':
                return 'Designated Route'
            elif tag[1] == 'customers':
                return 'Customer Access Only'
            elif tag[1] == 'delivery':
                return 'Delivery Access'

        if tag[0] == 'surveillance':
            if tag[1] == 'traffic':
                return 'Traffic Camera'
            else:
                return 'Surveillance Camera (' + tag[1] + ')'

        if tag[0] == 'landuse':
            if tag[1] == 'construction':
                return 'Construction Site'

        if tag[0] == 'noexit':
            if tag[1] == 'yes':
                return 'No Exit'

        if tag[0] == 'office':
            if tag[1] in ('nonprofit', 'non-profit', 'non_profit'):
                return 'Non Profit Organization Office'

        return u"{}: {}".format(tag[0], tag[1])

    def should_show_tag(self, tag, entity):

        if not tag:
            return False

        if tag[0].startswith('gnis:'):
            return False

        if tag[0] == 'image':
            return False  # Images are rendered - not displayed via paths

        if tag[0] == 'interval' and self.image:
            return False  # This is just used to auto-refresh the image

        if tag[0] in ('iff', 'layer'):
            return False

        if tag[0] == 'park_ride' and tag[1] == 'no':
            return False

        if tag[0] == 'area' and entity.has_tag('building'):
            return False

        if tag[0] == 'natural' and tag[1] == 'water' and entity.has_tag('water'):
            return False

        if tag[0] == 'sport' and entity.has_tag_value('leisure', 'pitch'):
            return False

        if tag[0] == 'contact:webcam':
            return False

        if tag[0] == 'man_made' and tag[1] == 'surveillance' and entity.has_tag('surveillance'):
            return False

        if tag[0] == 'building' and tag[1] == 'yes':
            if entity.has_tag('shop'):
                return False
            if entity.has_tag('amenity'):
                return False
            if entity.has_tag('leisure'):
                return False
            if entity.has_tag('sport'):
                return False

        return True

    def handle_key(self, key):

        if is_enter_key(key):
            self.application.select_page_by_index(0)
            return True

        return super(MapInfoPage, self).handle_key(key)





