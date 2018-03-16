import pygame
import time
import pygame.locals
import pygame.mixer
from random import randint

pygame.mixer.init()
pygame.mixer.music.load('Ray1.wav')
pygame.mixer.init(44100, -16,2,2048)
#pygame.mixer.music.load('Pop.wav')



class SpaceShip(pygame.sprite.Sprite):
    """ A spaceship sprite.
    params: size, which is a tuple of the width an height of the
    window in pixels.
    """

    def __init__(self, size):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('spaceship.png'), (60, 40))
        self.rect = self.image.get_rect()
        self.g = 1 / 9
        self.size = size
        self.vy = 0

    def update(self):
        """ Move the spaceship up and down with gravity.
            There is a terminal velocity as well as stopping on the
            screen boundaries.
        """

        # stop at top of screen
        if self.rect.top < 0:
            self.rect.top = 0

        # stop at bottom of screen
        elif self.rect.top > self.size[1] - self.rect.height:
            self.rect.top = self.size[1] - self.rect.height

        else:
            self.rect = self.rect.move(0, self.vy)

        # terminal velocity
        self.vy = 10 / 3 if self.vy >= 10 / 3 else self.vy + self.g


class KeyboardController:
    """ Control the ship with the keyboard. """

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Space to flap or restart the game. """
        if event.type != pygame.locals.KEYDOWN:
            return
        if event.key == pygame.K_SPACE:
            # Space either restarts the game or flaps the ship.
            if self.model.in_progress:
                self.model.spaceship.vy = -10 / 3
            else:
                self.model.reset()


class Jupiter(pygame.sprite.Sprite):
    """ Backdrop of jupiter"""

    def __init__(self, size):
        super().__init__()
        self.image = pygame.image.load('jupiter.png')
        self.rect = self.image.get_rect()
        self.rect.left = size[0]
        self.vx = 0.05
        self.x = size[0]

    def update(self):
        self.x -= self.vx
        self.rect.left = self.x


class Model:
    """ The model encompassing the state of the game. """

    def __init__(self, size):
        self.spaceship = SpaceShip(size)
        self.astroidBelt = AstroidBelt(99, size)
        self.in_progress = True
        self.jupiter = Jupiter(size)
        self.over_message = "Game Over, Hit Space!"

    def update(self):
        """ Update the state of the game. """

        # if collide with an unsafe astroid, stop the game.
        if pygame.sprite.spritecollide(self.spaceship, self.astroidBelt.unsafeAstroids, False):
            self.in_progress = False

        # remove the safe astroid once collided.
        safe_collide = pygame.sprite.spritecollide(
            self.spaceship, self.astroidBelt.safeAstroids, False)
        for astroid in safe_collide:
            self.astroidBelt.sound.play(loops=0)
            self.astroidBelt.astroids.remove(astroid)


        if self.in_progress:
            self.spaceship.update()
            self.astroidBelt.update()
            self.jupiter.update()


    def reset(self):
        self.astroidBelt = AstroidBelt(99, size)
        self.in_progress = True


class WindowView:
    """ A class which renders the scene. """

    def __init__(self, model, size):
        self.model = model
        self.size = size
        self.font = pygame.font.SysFont('monospace', 45)
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.screen.blit(self.model.jupiter.image, self.model.jupiter.rect)
        self.model.astroidBelt.astroids.draw(self.screen)

        # render the number options.
        for astroid in self.model.astroidBelt.astroids:
            self.screen.blit(self.font.render(
                str(astroid.num), True, (255, 255, 255)), (astroid.rect.left + 40, astroid.rect.top + 40))

        # render the probleem
        self.screen.blit(self.font.render(str(self.model.astroidBelt.prob.a) +
                                          " x " + str(self.model.astroidBelt.prob.b), True, (0, 0, 255)), (50, 20))

        self.screen.blit(self.font.render(
            str(int(self.model.astroidBelt.score)), True, (255, 255, 0)), (500, 20))

        self.screen.blit(self.model.spaceship.image, self.model.spaceship.rect)

        if not self.model.in_progress:
            self.screen.blit(self.font.render(
                self.model.over_message, True, (0, 255, 255)), (100, 200))
        pygame.display.update()


class Astroid(pygame.sprite.Sprite):
    """ A single astroid sprite.
    It contains a number to be rendered on it as well as the window
    dimensions as an iterable.
    """

    def __init__(self, num, size):
        super().__init__()
        self.num = num
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load('astroid.png'), (int(size[1] / 4), int(size[1] / 4)))
        self.rect = self.image.get_rect()


class MultProb:
    """ A randomly generated multiplication problem and answer
    choices..
    Its parameter is the maximum number which can show up in a
    problem.
    """

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.new_prob()

    def new_prob(self):
        """ Create a new problem. """
        self.a = randint(0, self.difficulty)
        self.b = randint(0, self.difficulty)
        self.ans = self.a * self.b
        self.generate_choices()

    def generate_choices(self):
        """ Generate choices """
        choices = []
        self.safe_lvl = randint(0, 3)
        for x in range(4):
            choice = self.ans
            # make choices all look viable by setting the last digit
            # as well as constraining the range.
            while choice == self.ans:
                choice = randint(self.a // 10 * self.b // 10 * 100, (self.a // 10 + 1)
                                 * (self.b // 10 + 1) * 100) // 10 * 10 + self.ans % 10
            choices.append(choice)
        choices.insert(self.safe_lvl, self.ans)
        self.choices = choices


class AstroidBelt:
    """ A class containing groups of astroids.
    difficulty is passed onto the multiplication problem.
    For convenience, the score of the game is also kept here.
    """

    def __init__(self, difficulty, size):
        self.difficulty = difficulty
        self.size = size
        self.prob = MultProb(self.difficulty)
        self.gen_astroids()
        self.score = 0
        self.x = size[0]
        self.vx = 2/3
        self.sound = pygame.mixer.Sound('Ray1.wav')

    def gen_astroids(self):
        """ Generate new astroids. """

        astroids = pygame.sprite.Group(
            *[Astroid(c, self.size) for c in self.prob.choices])

        # group of wrong answers
        self.unsafeAstroids = pygame.sprite.Group()

        # group of correct answers.
        self.safeAstroids = pygame.sprite.Group()
        for i, astroid in enumerate(astroids):
            if i != self.prob.safe_lvl:
                self.unsafeAstroids.add(astroid)
            else:
                self.safeAstroids.add(astroid)
        for n, astroid in enumerate(astroids):
            astroid.rect.top = self.size[1] / 4 * n
            astroid.rect.left = self.size[0]
        self.astroids = astroids

    def update(self):
        """ move astroids over with constant speed, wrapping around
        the screen.
        """
        for astroid in self.astroids:
            if self.x < -astroid.rect.width:
                self.score += 1 #Score increases by 1 per astroid
                self.difficulty += 1/4
                self.prob.new_prob()
                self.gen_astroids()
                self.vx += 0.01
                self.x = self.size[0]
            else:
                self.x -= self.vx / 4
                astroid.rect.left = self.x


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
