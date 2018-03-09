import pygame
import time
import pygame.locals


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('spaceship.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.g = 1 / 9
        self.size = size
        self.vy = 0

    def update(self):
        if self.rect.top < 0:
            self.rect.top = 0

        elif self.rect.top > self.size[1] - self.rect.height:
            self.rect.top = self.size[1] - self.rect.height

        else:
            self.rect = self.rect.move(0, self.vy)

        self.vy = 10 / 3 if self.vy >= 10 / 3 else self.vy + self.g


class KeyboardController:
    ''' Handles keyboard input for flappy nerd '''

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Space sets the nerd's velocity. """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_SPACE:
            self.model.spaceship.vy = -10 / 3


class Model:
    def __init__(self, size):
        self.spaceship = SpaceShip(size)

    def update(self):
        self.spaceship.update()


class WindowView:
    def __init__(self, model, size):
        self.model = model
        self.size = size
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.screen.blit(self.model.spaceship.image, self.model.spaceship.rect)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    model = Model(size)
    view = WindowView(model, size)
    running = True
    controller = KeyboardController(model)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(0.01)
    pygame.quit()
