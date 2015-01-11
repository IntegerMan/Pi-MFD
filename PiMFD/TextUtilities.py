__author__ = 'Matt Eland'


def render_text(display, font, text, left, top, color, background=None):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(top=top, left=left)

    if background is not None:
        display.surface.fill(background, rect=rect)

    display.surface.blit(text_surface, rect)
    return rect


def render_text_centered(display, font, text, left, top, color, background=None):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(left, top))

    if background is not None:
        display.surface.fill(background, rect=rect)

    display.surface.blit(text_surface, rect)
    return rect


