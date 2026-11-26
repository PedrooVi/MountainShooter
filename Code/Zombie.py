import pygame

from Code.Entity import Entity


class Zombie(Entity):
    def __init__(self, kind, frames, bottom):
        self.kind = kind
        self.frames = frames
        self.frame_index = 0
        self.anim_time = 0.0
        super().__init__(kind, frames[0], (0, 0))
        self.rect = frames[0].get_rect(bottomleft=(0, bottom))

    def update(self, dt, speed):
        center_x = self.rect.centerx - speed * dt
        bottom = self.rect.bottom
        self.anim_time += dt
        if self.anim_time >= 0.09:
            self.anim_time = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.surf = self.image
        self.rect = self.image.get_rect(centerx=int(center_x), bottom=bottom)

    def hitbox(self):
        width = max(24, round(self.rect.height * 0.38))
        height = round(self.rect.height * 0.85)
        return pygame.Rect(
            self.rect.centerx - width // 2,
            self.rect.bottom - height,
            width,
            height,
        )
