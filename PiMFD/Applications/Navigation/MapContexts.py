# coding=utf-8

"""
Map Contexts are used to provide contextual rendering and filtering information to the map as it is rendered
"""

__author__ = 'Matt Eland'


class MapContext(object):
    app = None

    def __init__(self, app):
        super(MapContext, self).__init__()

        self.app = app

    def should_show_lines(self, entity):
        return True

    def should_show_shapes(self, entity):
        return True

    def should_show_right_text(self, entity):
        return True

    def should_show_left_text(self, entity):
        return True

    def should_show_bottom_text(self, entity):
        return True

    def should_show_top_text(self, entity):
        return True
