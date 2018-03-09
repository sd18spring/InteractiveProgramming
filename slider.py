import pygame

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
        img = pygame.image.load('world-map.gif')
        white = (255, 64, 64)
        w = 100
        h = 100
        screen = pygame.display.set_mode((w, h))
        screen.fill((white))
        running = 1

        while running:
            screen.fill((white))
            screen.blit(img,(0,0))
            pygame.display.flip()
            for i in range(10):
                w = w+50
                h = h+50
                screen = pygame.display.set_mode((w, h))
                screen.fill((white))
                screen.blit(img,(0,0))
                pygame.display.flip()
                pygame.time.wait(2000)

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
