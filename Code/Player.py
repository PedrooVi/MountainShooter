import pygame

from Code.Assets import character
from Code.Const import (
    BODY_HEIGHT,
    BODY_LEFT,
    BODY_TOP,
    BODY_WIDTH,
    GRAVITY,
    GROUND_Y,
    JUMP_VELOCITY,
    PLAYER_ANCHOR_X,
    RUN_FRAME_TIME,
)
from Code.Entity import Entity


class Player(Entity):
    def __init__(self, name):
        frames = character(name)
        self.run_frames = frames["run"]
        self.jump_frames = frames["jump"]
        self.duck_frames = frames["duck"]
        self.frame_index = 0
        self.anim_time = 0.0
        self.foot_y = float(GROUND_Y)
        self.velocity_y = 0.0
        self.on_ground = True
        self.ducking = False
        self.coyote = 0.0
        self.jump_buffer = 0.0
        super().__init__(name, self.run_frames[0], (0, 0))
        self._place(self.run_frames[0])

    def update(self, dt, jump=False, duck=False):
        if jump:
            self.jump_buffer = 0.12
        else:
            self.jump_buffer = max(0.0, self.jump_buffer - dt)

        if self.on_ground:
            self.coyote = 0.1
        else:
            self.coyote = max(0.0, self.coyote - dt)

        if self.jump_buffer > 0 and (self.on_ground or self.coyote > 0):
            self.velocity_y = JUMP_VELOCITY
            self.on_ground = False
            self.ducking = False
            self.jump_buffer = 0.0
            self.coyote = 0.0

        if not self.on_ground:
            self.velocity_y += GRAVITY * dt
            self.foot_y += self.velocity_y * dt
            if self.foot_y >= GROUND_Y:
                self.foot_y = float(GROUND_Y)
                self.velocity_y = 0.0
                self.on_ground = True

        self.ducking = bool(duck and self.on_ground)

        self.anim_time += dt
        if self.on_ground and self.anim_time >= RUN_FRAME_TIME:
            self.anim_time = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.run_frames)

        if not self.on_ground:
            image = self._jump_image()
        elif self.ducking:
            image = self.duck_frames[self.frame_index % len(self.duck_frames)]
        else:
            image = self.run_frames[self.frame_index]
        self._place(image)

    def hitbox(self):
        if self.ducking and self.on_ground:
            return self.rect.inflate(-self.rect.width * 0.12, -self.rect.height * 0.08)
        rect = self.rect
        body = pygame.Rect(
            rect.left + rect.width * BODY_LEFT,
            rect.top + rect.height * BODY_TOP,
            rect.width * BODY_WIDTH,
            rect.height * BODY_HEIGHT,
        )
        return body.inflate(0, 8)

    def _jump_image(self):
        frames = self.jump_frames
        last = len(frames) - 1
        if self.velocity_y < -40:
            index = int((1 - min(1, abs(self.velocity_y) / abs(JUMP_VELOCITY))) * last * 0.45)
        elif self.velocity_y > 40:
            index = int(last * 0.45 + min(1, self.velocity_y / abs(JUMP_VELOCITY)) * last * 0.55)
        else:
            index = int(last * 0.45)
        return frames[max(0, min(last, index))]

    def _place(self, image):
        self.image = image
        self.surf = image
        self.rect = image.get_rect(midbottom=(PLAYER_ANCHOR_X, int(self.foot_y)))
