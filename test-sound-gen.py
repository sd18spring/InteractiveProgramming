import pygame

pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound('doublebass.wav')

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Testing')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('simplebutton.jpg')

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

x = (display_width * 0.45)
y = (display_height * 0.8)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    car(x,y)
    for i in range(display_width):
        for j in range(display_height):
            val = gameDisplay.get_at((i,j))
            if val == (238,4,15,255):
                sound.play()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
