# coding=utf-8
"""
Contains code useful for rendering images to the screen
"""
from StringIO import StringIO
import urllib2

import pygame
from pygame.rect import Rect

from PiMFD.UI.Panels import UIWidget


__author__ = 'Matt Eland'


class ImageRenderer(UIWidget):
    """
    A simple construct for a blank line
    """

    def __init__(self, display, page, surface, size=None):
        """

        :type size: tuple
        :type surface: pygame.Surface
        """
        super(ImageRenderer, self).__init__(display, page)

        self.surface = surface

        if size:
            self.width = size[0]
            self.height = size[1]
        else:
            self.width, self.height = surface.get_size()

    def render(self):
        """
        Renders the image to the screen
        """
        self.rect = self.set_dimensions_from_rect(Rect(self.pos[0], self.pos[1], self.width, self.height))

        self.display.surface.blit(self.surface, self.rect)

        return self.rect


class WebImageRenderer(ImageRenderer):
    def __init__(self, display, page, url, size=None, interval=0):
        """

        :type url: basestring
        :type size: tuple
        """

        self.interval = interval
        self.url = url

        surface = self.get_image_surface(url)

        # Let the core image Renderer take care of the rest of things from here on out
        super(WebImageRenderer, self).__init__(display, page, surface, size=size)

    def get_image_surface(self, url):
        # Grab the image data from the interwebs
        data = StringIO(urllib2.urlopen(url).read())

        # Build a surface-like object from the data
        adapter = StringIOImageAdapter(data)
        surface = pygame.image.load(adapter)

        return surface


class StringIOImageAdapter(object):
    def __init__(self, data):
        self.data = data.getvalue()
        self.pos = 0

    def read(self, size=None):
        start = self.pos
        end = len(self.data) - 1

        if size is not None:
            end = min(len(self.data), self.pos + size)

        self.pos = end
        return self.data[start:end]

    def seek(self, offset, whence=0):
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos = self.pos + offset
        elif whence == 2:
            self.pos = len(self.data) + offset

    def write(self):
        pass

    def tell(self):
        return self.pos


