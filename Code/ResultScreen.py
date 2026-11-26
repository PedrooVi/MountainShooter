import pygame

from Code.Background import Background
from Code.Const import COLOR_GREEN, COLOR_RED, COLOR_WHITE, COLOR_YELLOW, FPS, RESULT_OPTIONS, WIN_WIDTH
from Code.Ui import draw_text, present


class ResultScreen:
    def __init__(self, window, canvas, status, score):
        self.window = window
        self.canvas = canvas
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.status = status
        self.score = score
        self.option = 0

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_UP, pygame.K_s, pygame.K_w):
                        self.option = (self.option + 1) % len(RESULT_OPTIONS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return "retry" if self.option == 0 else "menu"
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"

            self.background.update(dt, 22)
            self._draw()
            present(self.window, self.canvas)

    def _draw(self):
        self.canvas.fill((0, 0, 0))
        self.background.draw(self.canvas)
        veil = pygame.Surface(self.canvas.get_size(), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 150))
        self.canvas.blit(veil, (0, 0))

        if self.status == "victory":
            draw_text(self.canvas, "VITORIA", 46, COLOR_GREEN, True, center=(WIN_WIDTH / 2, 70))
            draw_text(self.canvas, "Voce sobreviveu ao apocalipse.", 18, COLOR_WHITE, center=(WIN_WIDTH / 2, 112))
        else:
            draw_text(self.canvas, "FIM DE JOGO", 42, COLOR_RED, True, center=(WIN_WIDTH / 2, 70))
            draw_text(self.canvas, "Os zumbis alcancaram voce.", 18, COLOR_WHITE, center=(WIN_WIDTH / 2, 112))

        draw_text(self.canvas, f"PONTUACAO  {self.score}", 26, COLOR_YELLOW, True, center=(WIN_WIDTH / 2, 156))

        for index, label in enumerate(RESULT_OPTIONS):
            color = COLOR_YELLOW if index == self.option else COLOR_WHITE
            prefix = "> " if index == self.option else "  "
            draw_text(self.canvas, prefix + label, 20, color, True, center=(WIN_WIDTH / 2, 214 + index * 30))

        draw_text(self.canvas, "ENTER confirma    ESC volta ao menu", 15, COLOR_WHITE, center=(WIN_WIDTH / 2, 292))
