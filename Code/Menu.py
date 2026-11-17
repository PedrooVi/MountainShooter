from tkinter.font import Font

import pygame
from pygame import Rect
from pygame.surface import Surface

from Code.Const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTION, COLOR_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png')
        self.rect = self.surf.get_rect(left=0, top=0)


    def run (self):
        # Carregando e reproduzindo musica do menu
        pygame.mixer_music.load('./asset/menu.mp3')
        pygame.mixer_music.play(-1)
        while True:
            # CRIANDO IAMGEM INICIAL DO MENU
            self.window.blit(source=self.surf, dest=self.rect)
            #ADICIONANDO ESCRITA DE TEXTO NO MEUNU
            self.menu_text(50, "Mountain", COLOR_ORANGE, ((WIN_WIDTH /2),70 ))
            self.menu_text(50, "Shooter", COLOR_ORANGE, ((WIN_WIDTH / 2), 120))

            # ADICIONANDO OPCOES DO MENU
            # FOR PARA PERCORRER TODAS AS OPCOES DO MENU
            for i in range (len(MENU_OPTION)):
                self.menu_text(20, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH /2), 200 + 25 * i))

            pygame.display.flip()
            # Checando todos os ventos
            for event in pygame.event.get():
                 if(event.type == pygame.QUIT):
                     pygame.quit() # Fechar a janela
                     quit # Encerrar inicializacao do pygame


    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font =pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)