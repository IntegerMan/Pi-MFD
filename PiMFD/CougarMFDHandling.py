# coding=utf-8

"""
This file contains classes dealing with the handling of input buttons for the Cougar MFD panel.
"""
from PiMFD.UI import Keycodes

__author__ = 'Matt Eland'


class CougarMFDInputHandler(object):
    rotation_up = 0
    rotation_right = 1
    rotation_down = 2
    rotation_left = 3

    rotation = rotation_up

    def __init__(self, controller, rotation=rotation_up):
        super(CougarMFDInputHandler, self).__init__()

        self.controller = controller
        self.rotation = int(rotation)

    def handle_button_down(self, button):

        print(button)

        if self.rotation == self.rotation_right:
            self.handle_button_down_right(button)
        elif self.rotation == self.rotation_down:
            self.handle_button_down_down(button)
        elif self.rotation == self.rotation_left:
            self.handle_button_down_left(button)
        else:
            self.handle_button_down_up(button)

    def handle_button_down_up(self, button):

        if button in (0, 1, 2, 3, 4):  # MFD Top row - 0 left, 4 right
            self.controller.handle_button(button, True)
        elif button in (10, 11, 12, 13, 14):  # MFD Bottom row - 14 left, 10 right
            self.controller.handle_button(14 - button, False)
        elif button == 20:  # MFD SYM Up - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEUP)
        elif button == 21:  # MFD SYM Down - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEDOWN)
        elif button == 22:  # MFD CON Up - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_UP)
        elif button == 23:  # MFD CON Down - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_DOWN)
        elif button == 24:  # MFD BRT UP - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_LEFT)
        elif button == 25:  # MFD BRT DOWN - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_RIGHT)
        elif button == 21:  # MFD GAIN UP - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PLUS)
        elif button == 20:  # MFD GAIN DOWN - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_MINUS)
        elif button in (15, 16, 17, 18, 19):  # MFD Left - 15 bottom, 19 top
            pass
        elif button in (5, 6, 7, 8, 9):  # MFD Right - 9 bottom, 5 top
            self.controller.handle_keyboard_event(Keycodes.KEY_KP_ENTER)

    def handle_button_down_left(self, button):

        if button in (5, 6, 7, 8, 9):  # MFD Top row - 5 left, 9 right
            self.controller.handle_button(button - 5, True)
        elif button in (19, 18, 17, 16, 15):  # MFD Bottom row - 19 left, 15 right
            self.controller.handle_button(19 - button, False)
        elif button == 22:  # MFD SYM Up - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEUP)
        elif button == 23:  # MFD SYM Down - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEDOWN)
        elif button == 25:  # MFD CON Up - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_UP)
        elif button == 24:  # MFD CON Down - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_DOWN)
        elif button == 26:  # MFD BRT UP - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_LEFT)
        elif button == 27:  # MFD BRT DOWN - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_RIGHT)
        elif button == 21:  # MFD GAIN UP - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PLUS)
        elif button == 20:  # MFD GAIN DOWN - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_MINUS)
        elif button in (0, 1, 2, 3, 4):  # MFD Left - 4 bottom, 0 top
            pass
        elif button in (10, 11, 12, 13, 14):  # MFD Right - 4 bottom, 0 top
            self.controller.handle_keyboard_event(Keycodes.KEY_KP_ENTER)

    def handle_button_down_down(self, button):

        if button in (0, 1, 2, 3, 4):  # MFD Top row - 0 left, 4 right
            self.controller.handle_button(button, True)
        elif button in (10, 11, 12, 13, 14):  # MFD Bottom row - 14 left, 10 right
            self.controller.handle_button(14 - button, False)
        elif button == 20:  # MFD SYM Up - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEUP)
        elif button == 21:  # MFD SYM Down - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEDOWN)
        elif button == 22:  # MFD CON Up - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_UP)
        elif button == 23:  # MFD CON Down - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_DOWN)
        elif button == 24:  # MFD BRT UP - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_LEFT)
        elif button == 25:  # MFD BRT DOWN - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_RIGHT)
        elif button == 26:  # MFD GAIN UP - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PLUS)
        elif button == 27:  # MFD GAIN DOWN - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_MINUS)
        elif button in (15, 16, 17, 18, 19):  # MFD Left - 15 bottom, 19 top
            pass
        elif button in (5, 6, 7, 8, 9):  # MFD Right - 9 bottom, 5 top
            self.controller.handle_keyboard_event(Keycodes.KEY_KP_ENTER)

    def handle_button_down_right(self, button):

        if button in (5, 6, 7, 8, 9):  # MFD Top row - 15 left, 19 right
            self.controller.handle_button(button - 5, True)
        elif button in (9, 8, 7, 6, 5):  # MFD Bottom row - 9 left, 5 right
            self.controller.handle_button(9 - button, False)
        elif button == 23:  # MFD SYM Up - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEUP)
        elif button == 22:  # MFD SYM Down - Upper right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PAGEDOWN)
        elif button == 20:  # MFD CON Up - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_UP)
        elif button == 21:  # MFD CON Down - lower right corner
            self.controller.handle_keyboard_event(Keycodes.KEY_DOWN)
        elif button == 23:  # MFD BRT UP - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_LEFT)
        elif button == 22:  # MFD BRT DOWN - lower left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_RIGHT)
        elif button == 26:  # MFD GAIN UP - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_PLUS)
        elif button == 27:  # MFD GAIN DOWN - Upper left corner
            self.controller.handle_keyboard_event(Keycodes.KEY_MINUS)
        elif button in (10, 11, 12, 13, 14):  # MFD Left - 10 bottom, 14 top
            pass
        elif button in (0, 1, 2, 3, 4):  # MFD Right - 4 bottom, 0 top
            self.controller.handle_keyboard_event(Keycodes.KEY_KP_ENTER)