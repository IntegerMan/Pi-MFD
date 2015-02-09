# coding=utf-8
"""
Contains code useful for rendering images to the screen
"""
from StringIO import StringIO
from datetime import datetime
import urllib2

import pygame
from pygame.rect import Rect

from PiMFD.UI.Panels import UIWidget


__author__ = 'Matt Eland'


class ImageRenderer(UIWidget):
    """
    Handles image rendering as a widget
    """

    max_width = None
    min_width = None
    desired_width = None
    desired_height = None

    def __init__(self, display, page, surface, size=None, min_width=None, max_width=None):
        """
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        :type page: PiMFD.Applications.MFDPage.MFDPage
        :type size: tuple
        :type surface: pygame.Surface
        :type max_width: int
        :type min_width: int
        """
        super(ImageRenderer, self).__init__(display, page)

        self.surface = surface

        self.min_width = min_width
        self.max_width = max_width

        if size:
            self.desired_width = size[0]
            self.desired_height = size[1]

    def render(self):
        """
        Renders the image to the screen
        """

        image_size = self.surface.get_size()

        if self.desired_width:
            self.width = self.desired_width
        else:
            self.width = image_size[0]

        if self.desired_height:
            self.height = self.desired_height
        else:
            self.height = image_size[1]

        # Ensure width <= max_width when max width present
        if self.max_width and self.max_width < self.width:
            scale_factor = self.max_width / float(self.width)
            self.width = self.max_width
            self.height = int(self.height * scale_factor)

        # Ensure width >= min_width when min width present
        if self.min_width and self.min_width > self.width:
            scale_factor = self.min_width / float(self.width)
            self.width = self.min_width
            self.height = int(self.height * scale_factor)

        # If we need to scale, perform the scale now
        if self.width != image_size[0]:
            self.surface = pygame.transform.scale(self.surface, (self.width, self.height))

        self.rect = self.set_dimensions_from_rect(Rect(self.pos[0], self.pos[1], self.width, self.height))

        self.display.surface.blit(self.surface, self.rect)

        return self.rect


class WebImageRenderer(ImageRenderer):
    def __init__(self, display, page, url, size=None, interval=0, min_width=None, max_width=None):
        """
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        :type page: PiMFD.Applications.MFDPage.MFDPage
        :type size: tuple
        :type max_width: int
        :type min_width: int
        :type url: str
        """

        self.interval = int(interval)
        self.url = url

        surface = self.get_image_surface()
        self.last_fetch = datetime.now()

        # Let the core image Renderer take care of the rest of things from here on out
        super(WebImageRenderer, self).__init__(display, page, surface, size=size, max_width=max_width, min_width=min_width)

    def get_image_surface(self):

        # Grab the image data from the interwebs
        data = StringIO(urllib2.urlopen(self.url).read())

        self.last_fetch = datetime.now()

        # Build a surface-like object from the data
        adapter = StringIOImageAdapter(data)
        surface = pygame.image.load(adapter)

        return surface

    def render(self):

        # Auto-Refresh periodically
        if self.interval > 0:
            delta = datetime.now() - self.last_fetch

            if delta.seconds > self.interval:
                self.surface = self.get_image_surface()

        # Let the base class
        return super(WebImageRenderer, self).render()


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


