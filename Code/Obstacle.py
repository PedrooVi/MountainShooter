import pygame

from Code.Const import GROUND_Y
from Code.Entity import Entity


class Obstacle(Entity):
    def __init__(self, start_x):
        self.position_x = float(start_x)
        image = pygame.Surface((58, 56), pygame.SRCALPHA)
        pygame.draw.polygon(image, (35, 40, 42), [(8, 24), (50, 24), (56, 46), (2, 46)])
        pygame.draw.polygon(image, (220, 112, 52), [(7, 12), (51, 12), (49, 34), (9, 34)])
        pygame.draw.polygon(image, (244, 224, 179), [(13, 13), (21, 13), (17, 33), (10, 33)])
        pygame.draw.polygon(image, (244, 224, 179), [(35, 13), (43, 13), (39, 33), (32, 33)])
        pygame.draw.polygon(image, (55, 59, 58), [(12, 34), (19, 34), (16, 54), (9, 54)])
        pygame.draw.polygon(image, (55, 59, 58), [(41, 34), (48, 34), (51, 54), (44, 54)])
        pygame.draw.circle(image, (45, 48, 48), (13, 19), 2)
        pygame.draw.circle(image, (45, 48, 48), (45, 19), 2)
        super().__init__("road_barrier", image, (start_x, 0))
        self.rect = image.get_rect(left=start_x, bottom=GROUND_Y)

    def update(self, dt, speed):
        self.position_x -= speed * dt
        self.rect = self.image.get_rect(left=round(self.position_x), bottom=GROUND_Y)

    def hitbox(self):
        return self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.12)