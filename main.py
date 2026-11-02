import  pygame

# Incializacao de codigo
pygame.init()
# Criando interface do pygame no tamanho de 600X480 px
window = pygame.display.set_mode(size=(600, 480))
#Laco para manter janela aberta
while True:
    # Checando todos os ventos
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit() # Fechar a janela
            quit # Encerrar inicializacao do pygame