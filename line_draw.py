# import turtle
# from turtle import *
# from time import sleep
# turtle = Turtle()
# turtle.home()
# turtle.pensize(3)
# turtle.pencolor('white')
# turtle.ht()
# turtle.setposition(-450,0)
# screen = Screen()
# turtle.pencolor('black')
# turtle.st()
# screen.onscreenclick(turtle.goto)
# turtle.getscreen()._root.mainloop()


import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))


    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))


    keepGoing = True
    lineStart = (0, 0)
    drawColor = (0, 0, 0)
    lineWidth = 3

    while keepGoing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.line(background, drawColor, lineStart, lineEnd, lineWidth)
                    lineStart = lineEnd
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
