import pygame

from Code.Const import (
    COLOR_ROAD,
    COLOR_ROAD_EDGE,
    COLOR_ROAD_MARK,
    COLOR_SHADOW,
    GROUND_Y,
    WIN_HEIGHT,
    WIN_WIDTH,
)

_FONTS = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _FONTS:
        _FONTS[key] = pygame.font.SysFont("arial", size, bold=bold)
    return _FONTS[key]


def draw_text(surface, text, size, color, bold=False, shadow=True, **position):
    text_font = font(size, bold)
    text_surf = text_font.render(text, True, color)
    rect = text_surf.get_rect(**position)
    if shadow:
        shade = text_font.render(text, True, COLOR_SHADOW)
        surface.blit(shade, rect.move(1, 1))
    surface.blit(text_surf, rect)
    return rect


def present(window, canvas):
    pygame.transform.scale(canvas, window.get_size(), window)
    pygame.display.flip()


def draw_road(surface, offset):
    pygame.draw.rect(surface, COLOR_ROAD, (0, GROUND_Y, WIN_WIDTH, WIN_HEIGHT - GROUND_Y))
    pygame.draw.line(surface, COLOR_ROAD_EDGE, (0, GROUND_Y), (WIN_WIDTH, GROUND_Y), 2)
    mark_y = GROUND_Y + 18
    shift = int(offset) % 36
    x = -shift
    while x < WIN_WIDTH:
        pygame.draw.line(surface, COLOR_ROAD_MARK, (x, mark_y), (x + 16, mark_y), 2)
        x += 36


def draw_shadow(surface, center_x, foot_y, width):
    shadow = pygame.Surface((int(width), 12), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 80), shadow.get_rect())
    surface.blit(shadow, (center_x - width / 2, foot_y - 6))
