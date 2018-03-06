import pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
Astroid = pygame.image.load('Astroid.png').convert()
gameDisplay.blit(Astroid,(400,300))
pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
