import pygame

from Code.Assets import character
from Code.Background import Background
from Code.Const import CHARACTERS, COLOR_WHITE, COLOR_YELLOW, FPS, RUN_FRAME_TIME, WIN_WIDTH
from Code.Ui import draw_text, present


class CharacterSelect:
    def __init__(self, window, canvas, selected_name):
        self.window = window
        self.canvas = canvas
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.index = CHARACTERS.index(selected_name) if selected_name in CHARACTERS else 0
        self.frame = 0
        self.anim_time = 0.0

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.index = (self.index - 1) % len(CHARACTERS)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.index = (self.index + 1) % len(CHARACTERS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return CHARACTERS[self.index]
                    elif event.key == pygame.K_ESCAPE:
                        return None

            self.anim_time += dt
            if self.anim_time >= RUN_FRAME_TIME:
                self.anim_time = 0.0
                self.frame += 1
            self.background.update(dt, 24)
            self._draw()
            present(self.window, self.canvas)

    def _draw(self):
        self.canvas.fill((0, 0, 0))
        self.background.draw(self.canvas)
        veil = pygame.Surface(self.canvas.get_size(), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 90))
        self.canvas.blit(veil, (0, 0))
        draw_text(self.canvas, "ESCOLHA O PERSONAGEM", 26, COLOR_YELLOW, True, center=(WIN_WIDTH / 2, 28))

        for index, name in enumerate(CHARACTERS):
            center_x = WIN_WIDTH * (0.28 if index == 0 else 0.72)
            selected = index == self.index
            panel = pygame.Surface((168, 176), pygame.SRCALPHA)
            panel.fill((8, 10, 16, 170))
            panel_rect = panel.get_rect(center=(center_x, 148))
            self.canvas.blit(panel, panel_rect)
            border = COLOR_YELLOW if selected else (90, 96, 110)
            pygame.draw.rect(self.canvas, border, panel_rect, 3 if selected else 1)

            frames = character(name)["run"]
            image = frames[self.frame % len(frames)]
            preview_scale = min(
                (panel_rect.width - 24) / image.get_width(),
                (panel_rect.height - 52) / image.get_height(),
            )
            preview_size = (
                int(image.get_width() * preview_scale),
                int(image.get_height() * preview_scale),
            )
            preview = pygame.transform.scale(image, preview_size)
            image_rect = preview.get_rect(midbottom=(center_x, panel_rect.bottom - 36))
            self.canvas.blit(preview, image_rect)
            color = COLOR_YELLOW if selected else COLOR_WHITE
            draw_text(self.canvas, name.upper(), 20, color, True, center=(center_x, panel_rect.bottom - 18))

        draw_text(
            self.canvas,
            "SETAS escolhem    ENTER confirma    ESC volta",
            15,
            COLOR_WHITE,
            center=(WIN_WIDTH / 2, 292),
        )
