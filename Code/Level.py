import random

import pygame

from Code.Background import Background
from Code.Const import (
    AIR_CHANCE_END,
    AIR_CHANCE_START,
    BASE_SPEED,
    COLOR_WHITE,
    COLOR_YELLOW,
    DIFFICULTY_TIME,
    FIRST_SPAWN_DELAY,
    FPS,
    MAX_SPEED,
    MIN_SPAWN_GAP,
    OBSTACLE_CHANCE,
    SCORE_PER_SECOND,
    SPAWN_INTERVAL_END,
    SPAWN_INTERVAL_START,
    WIN_HEIGHT,
    WIN_SCORE,
    WIN_WIDTH,
)
from Code.EntityFactory import EntityFactory
from Code.Ui import draw_road, draw_shadow, draw_text, present


class Level:
    def __init__(self, window, canvas, character_name):
        self.window = window
        self.canvas = canvas
        self.character_name = character_name
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player = EntityFactory.create_player(character_name)
        self.zombies = []
        self.obstacles = []
        self.elapsed = 0.0
        self.score = 0.0
        self.spawn_timer = SPAWN_INTERVAL_START - FIRST_SPAWN_DELAY
        self.road_offset = 0.0
        self.last_kind = None
        self.same_kind = 0

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            jump = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu", int(self.score)
                    if event.key == pygame.K_SPACE:
                        jump = True

            pressed = pygame.key.get_pressed()
            duck = pressed[pygame.K_DOWN] or pressed[pygame.K_s]
            speed, interval, air_chance = self._difficulty()

            self.background.update(dt, speed)
            self.road_offset = (self.road_offset + speed * dt) % 36
            self.player.update(dt, jump, duck)
            for zombie in self.zombies:
                zombie.update(dt, speed * 1.04)
            self.zombies = [zombie for zombie in self.zombies if zombie.rect.right > -30]
            for obstacle in self.obstacles:
                obstacle.update(dt, speed)
            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.rect.right > -30]

            self.elapsed += dt
            self._spawn(dt, interval, air_chance)

            if self._hit():
                return "gameover", int(self.score)

            self.score += SCORE_PER_SECOND * dt
            if self.score >= WIN_SCORE:
                return "victory", WIN_SCORE

            self._draw()
            present(self.window, self.canvas)

    def _difficulty(self):
        progress = min(1.0, self.elapsed / DIFFICULTY_TIME)
        speed = BASE_SPEED + (MAX_SPEED - BASE_SPEED) * progress
        interval = SPAWN_INTERVAL_START + (SPAWN_INTERVAL_END - SPAWN_INTERVAL_START) * progress
        air_chance = AIR_CHANCE_START + (AIR_CHANCE_END - AIR_CHANCE_START) * progress
        return speed, interval, air_chance

    def _spawn(self, dt, interval, air_chance):
        self.spawn_timer += dt
        if self.spawn_timer < interval:
            return
        if not self._gap_is_safe():
            return
        self.spawn_timer = 0.0
        if random.random() < OBSTACLE_CHANCE:
            self.obstacles.append(EntityFactory.create_obstacle())
        else:
            self.zombies.append(EntityFactory.create_zombie(self._pick_kind(air_chance)))

    def _gap_is_safe(self):
        threats = self.zombies + self.obstacles
        if not threats:
            return True
        rightmost = max(threat.rect.right for threat in threats)
        return rightmost < WIN_WIDTH - MIN_SPAWN_GAP

    def _pick_kind(self, air_chance):
        kind = "air" if random.random() < air_chance else "ground"
        if kind == self.last_kind:
            self.same_kind += 1
        else:
            self.last_kind = kind
            self.same_kind = 1
        if self.same_kind > 3:
            kind = "air" if kind == "ground" else "ground"
            self.last_kind = kind
            self.same_kind = 1
        return kind

    def _hit(self):
        player_box = self.player.hitbox()
        for zombie in self.zombies:
            if player_box.colliderect(zombie.hitbox()):
                return True
        for obstacle in self.obstacles:
            if player_box.colliderect(obstacle.hitbox()):
                return True
        return False

    def _draw(self):
        self.canvas.fill((0, 0, 0))
        self.background.draw(self.canvas)
        draw_road(self.canvas, self.road_offset)
        draw_shadow(self.canvas, self.player.rect.centerx, int(self.player.foot_y), 46)
        for zombie in self.zombies:
            if zombie.kind == "ground":
                draw_shadow(self.canvas, zombie.rect.centerx, zombie.rect.bottom, zombie.rect.width * 0.7)
            self.canvas.blit(zombie.image, zombie.rect)
        for obstacle in self.obstacles:
            draw_shadow(self.canvas, obstacle.rect.centerx, obstacle.rect.bottom, obstacle.rect.width * 0.7)
            self.canvas.blit(obstacle.image, obstacle.rect)
        self.canvas.blit(self.player.image, self.player.rect)
        draw_text(
            self.canvas,
            f"PONTOS  {int(self.score):04d}",
            18,
            COLOR_YELLOW,
            True,
            topleft=(12, 8),
        )
        draw_text(
            self.canvas,
            f"META  {WIN_SCORE}",
            18,
            COLOR_WHITE,
            True,
            topright=(WIN_WIDTH - 12, 8),
        )
        draw_text(
            self.canvas,
            "ESPACO pula    S ou SETA BAIXO abaixa    ESC menu",
            13,
            COLOR_WHITE,
            midbottom=(WIN_WIDTH / 2, WIN_HEIGHT - 6),
        )
