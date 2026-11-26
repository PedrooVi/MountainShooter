import pygame

from Code.Assets import load
from Code.CharacterSelect import CharacterSelect
from Code.Const import WIN_HEIGHT, WIN_WIDTH, WINDOW_SCALE
from Code.Level import Level
from Code.Menu import Menu
from Code.ResultScreen import ResultScreen


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Zombie Runner")
        self.window = pygame.display.set_mode((WIN_WIDTH * WINDOW_SCALE, WIN_HEIGHT * WINDOW_SCALE))
        self.canvas = pygame.Surface((WIN_WIDTH, WIN_HEIGHT)).convert_alpha()
        load()
        self.character = "Shinobi"

    def run(self):
        while True:
            menu = Menu(self.window, self.canvas)
            if menu.run() == "quit":
                pygame.quit()
                return

            back_to_menu = False
            while not back_to_menu:
                chosen = CharacterSelect(self.window, self.canvas, self.character).run()
                if chosen is None:
                    break
                self.character = chosen

                playing = True
                while playing:
                    status, score = Level(self.window, self.canvas, self.character).run()
                    if status == "menu":
                        playing = False
                        back_to_menu = True
                        continue
                    decision = ResultScreen(self.window, self.canvas, status, score).run()
                    if decision == "retry":
                        continue
                    playing = False
                    back_to_menu = True
