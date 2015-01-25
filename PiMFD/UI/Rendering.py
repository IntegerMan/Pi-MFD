# coding=utf-8
"""
Contains various helper methods for rendering
"""
import pygame

__author__ = 'Matt Eland'


def draw_horizontal_line(display_manager, color, x1, x2, y, surface=None):
    """
    Renders a horizontal line along a single vertical plane
    :param display_manager: The DisplayManager
    :type color: The RGB value to render
    :type x1: int the starting X coordinate of the line
    :type x2: int the ending X coordinate of the line
    :type y: int the Y coordinate for both ends of the line
    :param surface: The surface to render to. Defaults to the primary surface.
    """
    if surface is None:
        surface = display_manager.surface

    pygame.draw.line(surface, color, (x1, y), (x2, y))


def draw_vertical_line(display_manager, color, x, y1, y2, surface=None):
    """
    Renders a vertical line along a single horizontal plane
    :param display_manager: The DisplayManager
    :type color: The RGB value to render
    :type x: int the X coordinate for both ends of the line
    :type y1: int the starting X coordinate of the line
    :type y2: int the ending X coordinate of the line
    :param surface: The surface to render to. Defaults to the primary surface.
    """
    if surface is None:
        surface = display_manager.surface

    pygame.draw.line(surface, color, (x, y1), (x, y2))


def render_rectangle(display_manager, color, rect, width=1, surface=None):
    """
    Draws a rectangle
    :param display_manager: The DisplayManager
    :param color: The color to use to draw
    :param rect: The bounds of the rectangle
    :param width: The width of the rectangle. If 0, this will be a solid fill. Defaults to 1.
    :param surface: The surface to render to. Defaults to the primary surface.
    """
    if surface is None:
        surface = display_manager.surface

    pygame.draw.rect(surface, color, rect, width)


def render_circle(display_manager, color, center_pos, radius, width=1):
    """
    Renders a circle
    :param display_manager: The display manager
    :param color: The color to use for the circle
    :param center_pos: A point indicating the center of the circle
    :param radius: The radius of the circle
    :param width: The thickness of the circle's edge or 0 for fill
    :return: A Rect indicating the bounds of the drawn areas
    """
    return pygame.draw.circle(display_manager.surface, color, center_pos, radius, width)


def render_diamond(display_manager, color, center_pos, radius, width=1):
    """
    Renders a diamond
    :param display_manager: The display manager
    :param color: The color to use for the shape
    :param center_pos: A point indicating the center of the diamond
    :param radius: The distance from the center of the diamond to each of the four colors
    :param width: The thickness of the diamond or 0 for fill
    :return: A Rect indicating the bounds of the drawn areas
    """

    x = center_pos[0]
    y = center_pos[1]

    points = ((x - radius, y), (x, y - radius), (x + radius, y), (x, y + radius))

    return pygame.draw.polygon(display_manager.surface, color, points, width)


def render_text(display_manager, font, text, left, top, color, background=None, surface=None):
    """
    Renders text to the screen at the specified coordinates with the specified display parameters
    :param display_manager: The DisplayManager
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
        surface = display_manager.surface

    if background:
        surface.fill(background, rect=rect)

    surface.blit(text_surface, rect)
    return rect


def render_text_centered(display_manager, font, text, left, top, color, background=None, surface=None):
    """
    Renders text centered horizontally around the specified points
    :param display_manager: The DisplayManager
    :type font: pygame.ftfont.Font The font used to render the text
    :type text: str The text to render
    :type left: int The x coordinate for the center of the text block
    :type top: int The y coordinate for the top of the text block
    :type color: tuple The RGB color to render the text using
    :type background: unknown or tuple The RGB color to render the background or None (default) for transparent
    :param surface: The surface to render to. Defaults to the primary surface.
    :return: A Rect representing the rendered area for the text
    """
    text_surface = font.font.render(text, True, color)
    rect = text_surface.get_rect(center=(left, top + (font.measure(text)[1] / 2)))

    if surface is None:
        surface = display_manager.surface

    if background:
        surface.fill(background, rect=rect)

    surface.blit(text_surface, rect)
    return rect


def to_rgba(color, alpha=255):
    """
    Takes a RGB color tuple and adds an alpha value to it
    :param color: The RGB color
    :param alpha: The alpha value (0-255)
    :return: A RGBA color structure
    """
    return color[0], color[1], color[2], alpha


def to_enabled_disabled(condition):
    """
    Returns 'Enabled' if the condition is True, otherwise returns 'Disabled'
    :param condition: The condition
    :return: 'Enabled' if the condition is True, otherwise returns 'Disabled'
    """
    if condition:
        return "Enabled"
    else:
        return "Disabled"