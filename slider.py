import pygame
import sys
import mydraws
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
        pics=['world-map.gif','loki.jpg','sonic.png','index.jpeg']
        img = pygame.image.load('world-map.gif')

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
        textsurface = myfont.render('2000               |2001               |2002               |2003               |2004               |2005               |2006               |2007               |2008               |2009               |2010               |2011               |2012               |2013               |2014               |2015               |2016', False, (0, 0, 0))
        screen.blit(textsurface,(0,670))

        running = True

        while running:

            if  0<=self.slidey.rect.x+100<125:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen, (255,0,0))
                pygame.display.flip()

            if  125<=self.slidey.rect.x+100<250:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,255,0))
                pygame.display.flip()

            if  250<=self.slidey.rect.x+100<375:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,0,255))
                pygame.display.flip()

            if  375<=self.slidey.rect.x+100<500:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(255,255,0))
                pygame.display.flip()

            if  500<=self.slidey.rect.x+100<625:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,255,255))
                pygame.display.flip()

            if  625<=self.slidey.rect.x+100<750:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(255,0,255))
                pygame.display.flip()

            if  750<=self.slidey.rect.x+100<875:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(192,192,192))
                pygame.display.flip()

            if  875<=self.slidey.rect.x+100<1000:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(128,128,128))
                pygame.display.flip()

            if  1000<=self.slidey.rect.x+100<1125:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(128,0,0))
                pygame.display.flip()

            if  1125<=self.slidey.rect.x+100<1250:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(128,128,0))
                pygame.display.flip()

            if  1250<=self.slidey.rect.x+100<1375:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,128,0))
                pygame.display.flip()

            if  1375<=self.slidey.rect.x+100<1500:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(128,0,128))
                pygame.display.flip()

            if  1500<=self.slidey.rect.x+100<1625:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,128,128))
                pygame.display.flip()

            if  1625<=self.slidey.rect.x+100<1750:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,0,128))
                pygame.display.flip()

            if  1750<=self.slidey.rect.x+100<1875:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(0,100,0))
                pygame.display.flip()

            if  1875<=self.slidey.rect.x+100:
                screen.fill((white))
                screen.blit(self.slidey.image, (self.slidey.rect.x, self.slidey.rect.y))
                screen.blit(textsurface,(0,950))
                pygame_draw_country.draw_map(screen,(46,139,87))
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

                last_mouse_in_state = False
                for country in pygame_draw_country.countries:
                            # Is the mouse inside the state?
                    mouse_in_state = any(pygame_draw_country.point_in_polygon(pygame.mouse.get_pos(), polygon) for polygon in wold_map.countries[country])
                            # Only print a message if the mouse moved from the inside to the outside, or vice versa
                    if mouse_in_state != last_mouse_in_state:
                        last_mouse_in_state = mouse_in_state
                        if mouse_in_state:
                            print ('mouse in',country)


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
    MainWindow = PyManMain()
    MainWindow.MainLoop()
