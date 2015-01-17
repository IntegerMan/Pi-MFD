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


def draw_rectangle(display_manager, color, rect, width=1, surface=None):
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
