import  pygame

from Code.Const import WIN_WIDTH, WIN_HEIGTH
from Code.Menu import Menu


class Game:
    def __init__(self):
        ##Incializacao de codigo
        pygame.init()
        # Criando interface do pygame
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGTH))

    def run(self):

        #Laco para manter janela aberta
        while True:
            menu = Menu(self.window)
            menu.run()
            pass
