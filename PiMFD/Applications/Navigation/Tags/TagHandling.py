# coding=utf-8

"""
Defines the TagHandler base class
"""

__author__ = 'Matt Eland'


class TagHandler(object):
    context = None

    def __init__(self, context):
        super(TagHandler, self).__init__()

        self.context = context

    def get_description_text(self, entity, value):
        return None

    def get_color(self, entity, value, cs):
        return None


class TagHandlerManager(object):
    handlers = {}
    context = None

    def __init__(self, context):
        super(TagHandlerManager, self).__init__()

        self.context = context

    def get_handler(self, key):

        if key in self.handlers:
            return self.handlers[key]
        else:
            return None

    def add_handler(self, key, handler):
        self.handlers[key] = handler

    def get_color(self, key, entity, cs):

        handler = self.get_handler(key)

        if handler:
            color = handler.get_color(entity, entity.get_tag_value(key), cs)
            if color:
                return color

        return None
