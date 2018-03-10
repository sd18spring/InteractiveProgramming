import pygame
import sys

class PyManMain:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))

    def MainLoop(self):
        pics=['world-map.gif','loki.jpg','sonic.png','index.jpeg']
        img = pygame.image.load('world-map.gif')

        rectangle_draging=False

        self.slidey=Slider()
        self.slidey_sprites = pygame.sprite.RenderPlain((self.slidey))

        white = (255, 64, 64)
        w = 1200
        h = 700
        screen = pygame.display.set_mode((w, h))
        screen.fill((white))

        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 28)
        textsurface = myfont.render('   2000 |  2001  |  2002  |  2003  |  2004  |  2005  |  2006  |  2007  |  2008  |  2009  |  2010  |  2011  |  2012  |  2013  |  2014  |  2015  |  2016', False, (0, 0, 0))
        screen.blit(textsurface,(0,670))

        running = True

        while running:

            if  0<=self.slidey.rect.x<300:
                screen.fill((white))
                screen.blit(img,(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,670))
                pygame.display.flip()

            if 300<=self.slidey.rect.x<600:
                screen.fill((white))
                screen.blit(pygame.image.load('loki.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,670))
                pygame.display.flip()

            if 600<=self.slidey.rect.x<900:
                screen.fill((white))
                screen.blit(pygame.image.load('sonic.png'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,670))
                pygame.display.flip()

            if 900<=self.slidey.rect.x:
                screen.fill((white))
                screen.blit(pygame.image.load('index.jpeg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,670))
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.slidey.rect.collidepoint(event.pos):
                            rectangle_draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.slidey.rect.x - mouse_x
                            offset_y = self.slidey.rect.y - mouse_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        rectangle_draging = False

                elif event.type == pygame.MOUSEMOTION:
                    if rectangle_draging:
                        mouse_x, mouse_y = event.pos
                        self.slidey.rect.x = mouse_x + offset_x

class Slider(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color=(0,0,0), width=20, height=10):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x=0
       self.rect.y=690

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
