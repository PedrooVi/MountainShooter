import random

import pygame

from Code.Assets import cities
from Code.Const import FADE_TIME, SCENARIO_INTERVAL, WIN_WIDTH


class Background:
    """Cenario urbano em parallax, com troca suave entre as cidades."""

    def __init__(self):
        self.cities = cities()
        self.index = random.randrange(len(self.cities))
        self.offsets = [[0.0] * len(city) for city in self.cities]
        self.next_index = None
        self.fade = 0.0
        self.change_in = SCENARIO_INTERVAL

    def update(self, dt, speed):
        self._scroll(self.index, dt, speed)
        self.change_in -= dt
        if self.next_index is None and self.change_in <= 0:
            options = [i for i in range(len(self.cities)) if i != self.index]
            self.next_index = random.choice(options)
            self.fade = 0.0
        if self.next_index is not None:
            self._scroll(self.next_index, dt, speed)
            self.fade += dt / FADE_TIME
            if self.fade >= 1:
                self.index = self.next_index
                self.next_index = None
                self.fade = 0.0
                self.change_in = SCENARIO_INTERVAL

    def draw(self, surface):
        self._draw_city(surface, self.index, 255)
        if self.next_index is not None:
            self._draw_city(surface, self.next_index, int(255 * min(self.fade, 1)))

    def _scroll(self, index, dt, speed):
        count = len(self.cities[index])
        offsets = self.offsets[index]
        for layer_index in range(count):
            if count == 1:
                factor = 1.0
            else:
                factor = 0.12 + 0.88 * (layer_index / (count - 1))
            offsets[layer_index] = (offsets[layer_index] + speed * factor * dt) % WIN_WIDTH

    def _draw_city(self, surface, index, alpha):
        for layer, offset in zip(self.cities[index], self.offsets[index]):
            x = -int(offset)
            self._blit(surface, layer, x, alpha)
            self._blit(surface, layer, x + WIN_WIDTH, alpha)

    def _blit(self, surface, layer, x, alpha):
        if alpha >= 250:
            surface.blit(layer, (x, 0))
            return
        ghost = layer.copy()
        ghost.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(ghost, (x, 0))
