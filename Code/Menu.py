import pygame

from Code.Background import Background
from Code.Const import COLOR_GREEN, COLOR_ORANGE, COLOR_WHITE, COLOR_YELLOW, FPS, MENU_OPTIONS, WIN_WIDTH
from Code.Ui import draw_text, present


class Menu:
    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.option = 0

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.option = (self.option + 1) % len(MENU_OPTIONS)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.option = (self.option - 1) % len(MENU_OPTIONS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return "start" if self.option == 0 else "quit"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"

            self.background.update(dt, 28)
            self._draw()
            present(self.window, self.canvas)

    def _draw(self):
        self.canvas.fill((0, 0, 0))
        self.background.draw(self.canvas)
        veil = pygame.Surface(self.canvas.get_size(), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 110))
        self.canvas.blit(veil, (0, 0))
        draw_text(self.canvas, "ZOMBIE", 42, COLOR_ORANGE, True, center=(WIN_WIDTH / 2, 52))
        draw_text(self.canvas, "RUNNER", 42, COLOR_GREEN, True, center=(WIN_WIDTH / 2, 96))

        for index, label in enumerate(MENU_OPTIONS):
            color = COLOR_YELLOW if index == self.option else COLOR_WHITE
            prefix = "> " if index == self.option else "  "
            draw_text(
                self.canvas,
                prefix + label,
                22,
                color,
                True,
                center=(WIN_WIDTH / 2, 158 + index * 28),
            )

        instructions = (
            "ESPACO: pular",
            "SETA PARA BAIXO ou S: abaixar",
            "ENTER: iniciar, confirmar ou reiniciar",
            "ESC: voltar ao menu ou sair",
            "SETAS: navegar nos menus e na selecao",
        )
        for index, line in enumerate(instructions):
            draw_text(self.canvas, line, 15, COLOR_WHITE, center=(WIN_WIDTH / 2, 230 + index * 16))
