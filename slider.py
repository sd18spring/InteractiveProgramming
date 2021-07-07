import pygame
import sys
import pygame_draw_country
import random
import wold_map

def random_color():
    r = lambda: random.randint(0,255)
    return (r(),r(),r())

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
        rectangle_draging=False

        self.slidey=Slider()
        self.slidey_sprites = pygame.sprite.RenderPlain((self.slidey))

        white = (255, 255, 255)
        w = 2000
        h = 1500
        screen = pygame.display.set_mode((w, h))
        screen.fill((white))

        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 28)
        textsurface = myfont.render('2001               |2002               |2003               |2004               |2005               |2006               |2007               |2008               |2009               |2010               |2011               |2012               |2013               |2014               |2015               |2016', False, (0, 0, 0))
        running = True

        while running:

            if  0<=self.slidey.rect.x+100<125:
                screen.fill((white))
                screen.blit(pygame.image.load('2001.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  125<=self.slidey.rect.x+100<250:
                screen.fill((white))
                screen.blit(pygame.image.load('2002.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  250<=self.slidey.rect.x+100<375:
                screen.fill((white))
                screen.blit(pygame.image.load('2003.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  375<=self.slidey.rect.x+100<500:
                screen.fill((white))
                screen.blit(pygame.image.load('2004.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  500<=self.slidey.rect.x+100<625:
                screen.fill((white))
                screen.blit(pygame.image.load('2005.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  625<=self.slidey.rect.x+100<750:
                screen.fill((white))
                screen.blit(pygame.image.load('2006.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  750<=self.slidey.rect.x+100<875:
                screen.fill((white))
                screen.blit(pygame.image.load('2007.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  875<=self.slidey.rect.x+100<1000:
                screen.fill((white))
                screen.blit(pygame.image.load('2008.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1000<=self.slidey.rect.x+100<1125:
                screen.fill((white))
                screen.blit(pygame.image.load('2009.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1125<=self.slidey.rect.x+100<1250:
                screen.fill((white))
                screen.blit(pygame.image.load('2010.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1250<=self.slidey.rect.x+100<1375:
                screen.fill((white))
                screen.blit(pygame.image.load('2011.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1375<=self.slidey.rect.x+100<1500:
                screen.fill((white))
                screen.blit(pygame.image.load('2012.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1500<=self.slidey.rect.x+100<1625:
                screen.fill((white))
                screen.blit(pygame.image.load('2013.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1625<=self.slidey.rect.x+100<1750:
                screen.fill((white))
                screen.blit(pygame.image.load('2014.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1750<=self.slidey.rect.x+100<1875:
                screen.fill((white))
                screen.blit(pygame.image.load('2015.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

            if  1875<=self.slidey.rect.x+100:
                screen.fill((white))
                screen.blit(pygame.image.load('2016.jpg'),(0,0))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame.display.update()

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
    def __init__(self, color=(0,0,0), width=100, height=50):
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
       self.rect.y=1000

if __name__ == "__main__":
    white = (255, 255, 255)
    w = 2000
    h = 1500
    years=['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011',
    '2012','2013','2014','2015','2016']
    screen = pygame.display.set_mode((w, h))
    screen.fill((white))
    for year in years:
        pygame_draw_country.draw_map(screen, year)
        pygame.image.save(screen, year+'.jpg')
        screen.fill((white))
    MainWindow = PyManMain()
    MainWindow.MainLoop()
