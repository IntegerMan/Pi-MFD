__author__ = 'Matt Eland'


class ColorScheme(object):
    def __init__(self, background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255)):
        self.background = background
        self.foreground = foreground
        self.highlight = highlight
        pass

    def clone_to(self, target):
        target.background = self.background
        target.foreground = self.foreground
        target.highlight = self.highlight
        return target

    background = (0, 0, 0)
    foreground = (0, 255, 0)
    highlight = (255, 255, 255)

    pass


class ColorSchemes(object):
    # A green based color scheme resembling military avionics displays
    military = ColorScheme(background=(0, 8, 0), foreground=(0, 255, 0), highlight=(255, 255, 255))

    # A cyan display
    cyan = ColorScheme(background=(0, 0, 32), foreground=(0, 170, 170), highlight=(0, 0, 255))

    pass

