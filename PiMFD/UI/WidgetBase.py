# coding=utf-8

"""
Contains the base UIWidget definition
"""

from pygame.rect import Rect

__author__ = 'Matt Eland'


class UIObject(object):
    """
    A base representation of a UI element that will need a reference to a display manager at some point
    """

    display = None
    desired_size = 0, 0

    def __init__(self, display):
        """
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        """
        super(UIObject, self).__init__()
        self.display = display

    # noinspection PyMethodMayBeStatic
    def arrange(self):
        """
        Measures the widget and returns desired dimensions
        :return: The size used for arrangement
        :rtype: tuple
        """

        return self.desired_size

    # noinspection PyMethodMayBeStatic
    def render(self):
        """
        Renders the widget to the screen
        :return: The rect of the control as it was rendered
        """

        pass


class UIWidget(UIObject):
    """
    Represents a basic UI widget that the system is capable of arranging and rendering.
    """

    # Basic Arrangement Attributes
    pos = (0, 0)
    size = (0, 0)
    left = 0
    right = 0
    top = 0
    bottom = 0
    width = 0
    height = 0
    rect = Rect(0, 0, 0, 0)
    page = None
    data_context = None
    is_highlighted = None
    parent = None

    def __init__(self, display, page):
        """
        :type page: PiMFD.UI.Pages.UIPage
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        """
        super(UIWidget, self).__init__(display)
        self.page = page

    def render_at(self, pos):
        """
        A convenience method to position and render the control in one statement
        :type pos: tuple
        :param pos: The position
        :return: The rect of the dimensions returned by render.
        """
        self.pos = pos
        return self.render()

    # noinspection PyMethodMayBeStatic
    def render(self):
        """
        Renders the widget to the screen
        :return: The rect of the control as it was rendered
        """
        return self.rect

    def set_dimensions_from(self, target):
        """
        Clones all dimension attributes from the target object
        :param target: The target to take values from
        :returns: Returns self.rect for convenience
        """
        self.pos = target.pos
        self.size = target.size
        self.left = target.left
        self.right = target.right
        self.top = target.top
        self.bottom = target.bottom
        self.width = target.width
        self.height = target.height
        self.rect = target.rect

        return self.rect
    
    def set_dimensions_from_rect(self, rect):
        """
        Copies dimensional attributes from the specified rect
        :type rect: pygame.Rect
        :param rect: The rectangle
        :returns: Returns self.rect for convenience
        """
        self.rect = rect
        self.pos = rect.x, rect.y
        self.size = rect.size
        self.left = rect.left
        self.right = rect.right
        self.top = rect.top
        self.bottom = rect.bottom
        self.width = rect.width
        self.height = rect.height

        return self.rect

