import pygame
from math import cos,sin,sqrt,radians,atan

pygame.init()

class GUI():
    WHITE = (255,255,255)
    font = pygame.font.SysFont("couriernew",32)
    bx = 150
    by = 100

    def __init__(self,gD):
        self.gD = gD

    def update(self,score):
        box = pygame.surface.Surface((self.bx, self.by))
        # txt_surf = self.font.render("score", True, self.WHITE)  # headline
        # txt_rect = txt_surf.get_rect(center=(self.bx//2, 30))
        # box.blit(txt_surf, txt_rect)
        txt_surf = self.font.render(str(score), True, self.WHITE)  # bottom line
        txt_rect = txt_surf.get_rect(center=(self.bx//2, 40))
        box.blit(txt_surf, txt_rect)
        self.gD.blit(box,(0,0))


def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    #DOES NOT WORK

    loc = image.get_rect().center  #rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    # rot_sprite.get_rect().center = loc
    rotRect = rot_sprite.get_rect()
    rotRect.center = loc
    return rot_sprite,rotRect

class Ship():
    """Ship class!
    Holds data on ship:
    angle (degress)
    x_speed
    y_speed
    x (position)
    y (position)
    oImage (img) original
    nImage (img) new
    drift (boolean)
    rect (pygame surface)

    """
    x_speed = 0
    y_speed = 0
    drift = False
    def __init__(self,x,y,angle,img,gD):
        """
        Initliazes with where the ship is facing as the angle
        """
        self.angle = angle
        self.x = x
        self.y = y
        self.oImage = img
        self.nImage = img
        self.w,self.h = img.get_size()
        self.gD = gD
        self.rect = img.get_rect()
    def move(self):
        """FORWARD!!!
        Moves the ship forward in the direction it's heading (its angle)
        """
        self.drift = False
        self.x_speed += cos(radians(self.angle))*.4
        self.y_speed += sin(radians(self.angle))*.4
        # if sqrt(self.x_speed**2+self.y_speed**2) < 10:

    def rotate(self,posNeg):
        """Rotates ship"""
        self.nImage,self.rect = rot_center(self.oImage,posNeg*3+(270-self.angle))
        self.angle -= posNeg*3

    def update(self):
        """MAGIC
        Does magic and makes the ship work.
        Updates position
        """
        width,height = self.gD.get_size()
        speed = sqrt(self.x_speed**2+self.y_speed**2)
        # print(speed)
        if speed < .08 and self.drift:
            self.drift = False
            self.x_speed = 0
            self.y_speed = 0
        if speed > 10:
            self.x_speed = cos(radians(self.angle))*10
            self.y_speed = sin(radians(self.angle))*10
        if self.drift:
            #theta = atan(self.y_speed/self.x_speed)
            self.x_speed *= .98
            self.y_speed *= .98

        self.y += self.y_speed
        self.x += self.x_speed

        if(self.x >= width):
            self.x = 0 - self.w
        elif(self.x <= 0 - self.w):
            self.x = width
        if(self.y >= height):
            self.y = 0 - self.h
        elif(self.y <= 0 - self.h):
            self.y = height

        self.rect.center = (self.x,self.y)

        self.gD.blit(self.nImage,self.rect)

class Asteroid():
    """
    Asteroid Class:
    x - position
    y - position
    speed - speed of asteroid
    direction - direction of asteroid
    image - surface containing picture of asteroid
    gameDisplay - the display to put the asteroid on
    w, h - the width and height of the surface
    """
    def __init__(self,x,y,speed,direction,gameDisplay):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load('Asteroid.png').convert()
        self.image.set_colorkey((0,0,0)) # Sets the Asteroids Blackness to be transparent
        self.w, self.h = self.image.get_size() # Gets the Asteroid's width and height
        self.destroyed = False
        self.gameDisplay = gameDisplay
    def update(self):
        """
        updates the position of the asteroid and rectangle
        """
        if(not self.destroyed): # once the asteroid is destroyed, it will stop redrawing the asteroid
            width, height = self.gameDisplay.get_size() # gets the display's width and length
            self.x = self.x + (self.speed * math.cos(self.direction))  # Sets the Asteroid's to a small change in space
            self.y = self.y + (self.speed * math.sin(self.direction))
            if(self.x >= width): # If the asteroid's coordinate goes outside of the window, set that coordinate to the other side of the map
                self.x = 0 - self.w  # adding the width of the image to make sure that the image doesn't appear suddenly (the image's position is the top right of the image)
            elif(self.x <= 0 - self.w): # same as above (makes it so that the whole image has to leave the screen for it to go to the other side)
                self.x = width
            if(self.y >= height):
                self.y = 0 - self.h
            elif(self.y <= 0 - self.h):
                self.y = height
            self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage)) # The Rect is for the hitbox
            self.gameDisplay.blit(self.image,(self.x,self.y)) # draws the asteroid on the screen
            #pygame.draw.rect(self.gameDisplay,(0,255,0),self.rect) # display's the asteroid's hit box in red (for testing)

class LargeAsteroid(Asteroid):

    """
    subclass of the asteroid, for the starting asteroids
    shrinkage - number that the rectangle hitbox shrinks by
    rect - the hitbox rectangle
    """
    def __init__(self,x,y,speed,direction,gameDisplay):
        super().__init__(x,y,speed,direction,gameDisplay)
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2)) # scales the asteroid to size
        self.w,self.h = self.image.get_size()
        self.shrinkage = 50
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage)) # lessening the hitbox so the corners don't stick out
    def destroy(self):
        """
        destroys the asteroid and returns the asteroids that should take it's place.
        """
        if(not self.destroyed):
            self.destroyed = True
            MedAster = []
            for i in range(2):
                MedAster.append(MediumAsteroid(self.x,self.y,self.speed*1.5,random.uniform(0,2*math.pi),self.gameDisplay)) #makes two more medium asteroids in it's place with random directions
            return MedAster
        return []
class MediumAsteroid(Asteroid):
    """
    subclass of the asteroid, for the second asteroid
    shrinkage - number that the rectangle hitbox shrinks by
    rect - the hitbox rectangle
    """
    def __init__(self,x,y,speed,direction,gameDisplay):
        super().__init__(x,y,speed,direction,gameDisplay)
        self.image = pygame.transform.scale(self.image,(self.w // 4,self.h // 4)) # half as big as large asteroid
        self.w,self.h = self.image.get_size()
        self.shrinkage = 25
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
    def destroy(self):
        """
        destroys the asteroid and returns the asteroids that should take it's place.
        """
        if(not self.destroyed):
            self.destroyed = True
            SmallAster = []
            for i in range(2):
                SmallAster.append(SmallAsteroid(self.x,self.y,self.speed*1.5,random.uniform(0,2*math.pi),self.gameDisplay)) #makes two more small asteroids in it's place with random directions
            return SmallAster
        return []
class SmallAsteroid(Asteroid):
    """
    subclass of the asteroid, for the last asteroid
    shrinkage - number that the rectangle hitbox shrinks by
    rect - the hitbox rectangle
    """
    def __init__(self,x,y,speed,direction,gameDisplay):
        super().__init__(x,y,speed,direction,gameDisplay)
        self.image = pygame.transform.scale(self.image,(self.w // 8,self.h // 8)) # half as big as medium asteroid
        self.w,self.h = self.image.get_size()
        self.shrinkage = 12
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
    def destroy(self):
        """
        destroys the asteroid and returns nothing because it is the smallest asteroid
        """
        self.destroyed = True
        return []
class CollectionOfAsteroids():
    def __init__(self,gameDisplay):
        self.listOfAsteroids = []
        self.gameDisplay = gameDisplay
        self.speed = 1
    def spawnAsteroids(self,numberOfAsteroids):
        width, height = self.gameDisplay.get_size()
        listOfAsteroids = [] # initializes a list of asteroids to update
        listOfRects = [] # initializes a list of hitboxes
        sampleAsteroid = LargeAsteroid(0,0,0,0,self.gameDisplay) # a sample asteroid to know where to spawn the asteroids in case we change the size later
        smallArea = 100 # the area that asteroids are to spawn around the the edge
        for i in range(numberOfAsteroids):
            side = random.randint(1,4)
            if(side == 1): # left side of the screen
                x = random.randint(-sampleAsteroid.w // 2,smallArea - sampleAsteroid.w // 2)
                y = random.randint(-sampleAsteroid.h // 2,height - sampleAsteroid.h // 2)
            elif(side == 2): # top side of the screen
                x = random.randint(-sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
                y = random.randint(-sampleAsteroid.w // 2,smallArea - sampleAsteroid.w // 2)
            elif(side == 3): # right side of the screen
                x = random.randint(width-smallArea - sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
                y = random.randint(-sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
            elif(side == 4): # bottom of the screen
                x = random.randint(-sampleAsteroid.w // 2,width - sampleAsteroid.w // 2)
                y = random.randint(height-smallArea - sampleAsteroid.w // 2,height - sampleAsteroid.w // 2)
            direction = random.uniform(0,math.pi * 2) # initiate each asteroid with a random direction
            listOfAsteroids.append(LargeAsteroid(x,y,self.speed,direction,self.gameDisplay))
            listOfRects.append(listOfAsteroids[i].rect)
        self.listOfAsteroids = listOfAsteroids
        self.listOfRects = listOfRects
    def update(self):
        listOfRects = [] # asteroid
        ListToDelete = [] # a list that incluedes the indicies of what to delete
        for i in range(len(self.listOfAsteroids)):
            if(self.listOfAsteroids[i].destroyed):
                ListToDelete.append(i) # if the asteroid is destroyed, remember the number to remove it later
            else:
                self.listOfAsteroids[i].update()
                listOfRects.append(self.listOfAsteroids[i].rect)
        for j in reversed(ListToDelete): # reversed so that it doesn't delete one and shift mid for loop.
            del self.listOfAsteroids[j]
        self.listOfRects = listOfRects
    def destroyAll(self): # function for testingasteroid, not for the real game
        sizeOfAsteroids = range(len(self.listOfAsteroids))
        for i in sizeOfAsteroids:
            newAsteroid = self.listOfAsteroids[i].destroy()
            if(newAsteroid != None):
                self.listOfAsteroids += newAsteroid # destroying all of the asteroids making them medium
        for i in sizeOfAsteroids:
            self.listOfAsteroids.pop(0)
class Projectile():
    def __init__(self,x,y,direction,alliance,gameDisplay):
        size = 3
        self.x = x
        self.y = y
        self.w = size
        self.h = size
        self.speed = 10
        self.direction = direction
        self.rect = ((self.x,self.y),(size,size))
        self.image = pygame.Surface((size,size))
        self.image.fill((255,255,255))
        self.gameDisplay = gameDisplay
        self.destroyed = False
        self.distanceTravelled = 0 # asteroids
        self.distanceWanted = 500 # the distance that the projectile travels before it is destroyed
        self.alliance = alliance
    def update(self):
        if(self.distanceTravelled < self.distanceWanted): # if the projectile has travelled farther than the wanted distance, it destroys itself
            width, height = self.gameDisplay.get_size() # gets the display's width and length
            self.x = self.x + (self.speed * math.cos(self.direction))  # Sets the speed to a small change in space
            self.y = self.y + (self.speed * math.sin(self.direction))
            self.distanceTravelled += self.speed # updates the disnance travelled
            if(self.x >= width): # If the projectile's coordinate goes outside of the window, set that coordinate to the other side of the map
                self.x = 0 - self.w  # adding the width of the image to make sure that the image doesn't appear suddenly (the image's position is the top right of the image)
            elif(self.x <= 0 - self.w): # same as above (makes it so that the whole image has to leave the screen for it to go to the other side)
                self.x = width
            if(self.y >= height):
                self.y = 0 - self.h
            elif(self.y <= 0 - self.h):
                self.y = height
            self.rect = pygame.Rect((self.x,self.y),(self.w,self.h))
            self.gameDisplay.blit(self.image,(self.x,self.y)) # draws the pixel on the screen
            #pygame.draw.rect(self.gameDisplay,(0,255,0),self.rect) # display's the projectile's hit box in green (for testing)
        else:
            self.destroy() # satisfying to right
    def destroy(self):
        self.destroyed = True
class CollectionOfProjectiles():
    def __init__(self,gameDisplay):
        self.listOfProjectiles = [] #initializes the asteroidprojectiles
        self.listOfRects = [] # initializes their hitboxes
        self.gameDisplay = gameDisplay
    def addProjectile(self,x,y,direction,alliance):
        self.listOfProjectiles.append(Projectile(x,y,direction,alliance,self.gameDisplay)) # The spacebar command should call this
                                            # with the x,y and directions of the ship (with an offset bc of the front of the ship and that the origin is top left)
    def update(self):
        ListToDelete = [] # initializes the indices of what to delete
        for i in range(len(self.listOfProjectiles)):
            if(self.listOfProjectiles[i].destroyed):
                ListToDelete.append(i) # adding the index of destroyed particles to delete
            else:
                self.listOfProjectiles[i].update()
        for j in reversed(ListToDelete):
            del self.listOfProjectiles[j]

class UFO():
    def __init__(self,y,FacingRight,gameDisplay,listOfProjectiles):
        self.y = y
        self.speed = 2
        self.destroyed = False
        self.image = pygame.image.load('UFO.gif').convert()
        self.image.set_colorkey((0,0,0))
        self.w, self.h = self.image.get_size()
        self.straight = bool(random.getrandbits(1))
        self.FacingRight = FacingRight
        self.gameDisplay = gameDisplay
        width, height = gameDisplay.get_size()
        self.counter = 0
        self.listOfProjectiles = listOfProjectiles
        if(FacingRight):
            self.x = -self.w
        else:
            self.x = width
    def update(self):
        if(self.counter % self.fireRate == 0):
            self.shoot()
        self.counter += 1
        width, height = self.gameDisplay.get_size()
        if(self.straight == True):
            if(self.FacingRight):
                self.direction = 0
            else:
                self.direction = math.pi
        else:
            if(self.FacingRight):
                if((self.x + self.w / 2) < width * 1 / 4):
                    self.direction = 0
                elif(self.x + self.w / 2 < width / 2):
                    self.direction = math.pi / 4
                else:
                    self.direction = - math.pi / 4
            else:
                if((self.x + self.w / 2) > width * 3 / 4):
                    self.direction = math.pi
                elif(self.x + self.w / 2 > width / 2):
                    self.direction = 5 * math.pi / 4
                else:
                    self.direction = 3 * math.pi / 4
        self.x = self.x + (self.speed * math.cos(self.direction))  # Sets the speed to a small change in space
        self.y = self.y + (self.speed * math.sin(self.direction))
        if(self.x >= width and self.FacingRight): # if the UFO goes out of the screen, destroy it
            self.destroyed = True
        elif(self.x <= 0 - self.w and not self.FacingRight):
            self.destroyed = True
        if(self.y >= height): # If the UFOs coordinate goes outside of the window, set that coordinate to the other side of the map
            self.y = 0 - self.h # adding the width of the image to make sure that the image doesn't appear suddenly (the image's position is the top right of the image)
        elif(self.y <= 0 - self.h): # same as above (makes it so that the whole image has to leave the screen for it to go to the other side)
            self.y = height
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
        #pygame.draw.rect(self.gameDisplay,(0,0,255),self.rect) # display's the asteroid's hit box in red (for testing)
        self.gameDisplay.blit(self.image,(self.x,self.y))
    def destroy(self):
        self.destroyed = True
class BigUFO(UFO):
    def __init__(self,y,FacingRight,gameDisplay,listOfProjectiles):
        super().__init__(y,FacingRight,gameDisplay,listOfProjectiles)
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2))
        self.w,self.h = self.image.get_size()
        self.shrinkage = 30
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
        self.fireRate = 60
    def shoot(self):
        if(not self.destroyed):
            self.listOfProjectiles.addProjectile(self.x + self.w / 2,self.y + self.h / 2,random.uniform(0,2*math.pi),"UFO")
class CollectionOfUFOs():
    def __init__(self,gameDisplay,listOfProjectiles):
        self.listOfUFOs = [] #initializes the projectiles
        self.listOfRects = [] # initializes their hitboxes
        self.gameDisplay = gameDisplay
        self.listOfProjectiles = listOfProjectiles
    def spawnBigUFO(self):
        width, height = self.gameDisplay.get_size()
        sampleUFO = BigUFO(0,True,self.gameDisplay,self.listOfProjectiles)
        y = random.randint(-sampleUFO.h // 2,height - sampleUFO.h // 2)
        facingRight = bool(random.getrandbits(1))
        self.listOfUFOs.append(BigUFO(y,facingRight,self.gameDisplay,self.listOfProjectiles))
    def update(self):
        listOfRects = []
        ListToDelete = [] # initializes the indices of what to delete
        for i in range(len(self.listOfUFOs)):
            if(self.listOfUFOs[i].destroyed):
                ListToDelete.append(i) # adding the index of destroyed particles to delete
            else:
                self.listOfUFOs[i].update()
                listOfRects.append(self.listOfUFOs[i].rect)
        for j in reversed(ListToDelete):
            del self.listOfUFOs[j]
        self.listOfRects = listOfRects
class listOfObjects():
    def __init__(self,gameDisplay):
        self.gameDisplay = gameDisplay
        self.Asteroids = CollectionOfAsteroids(gameDisplay)
        self.Projectiles = CollectionOfProjectiles(gameDisplay) # contains the CollectionOfAsteroids and CollectionOfProjectiles objects
        self.UFOs = CollectionOfUFOs(gameDisplay,self.Projectiles)
    def update(self):
        self.Asteroids.update()
        self.UFOs.update()
        self.Projectiles.update()
        for i in self.Projectiles.listOfProjectiles: # runs through each projectile
            collisionsAster = i.rect.collidelist(self.Asteroids.listOfRects) # detects if any of the asteroids are in contact with the projectile
            if (collisionsAster != -1): # if there is a collision
                self.Asteroids.listOfAsteroids += self.Asteroids.listOfAsteroids[collisionsAster].destroy() #destroy both the asteroid and the projectile.
                i.destroy()
            collisionsUFO = i.rect.collidelist(self.UFOs.listOfRects)
            if (collisionsUFO != -1 and i.alliance != "UFO"): # if there is a collision
                self.UFOs.listOfUFOs[collisionsUFO].destroy() #destroy both the asteroid and the projectile.
                i.destroy()
        for i in self.UFOs.listOfUFOs:
            collisionsAster = i.rect.collidelist(self.Asteroids.listOfRects) # detects if any of the asteroids are in contact with the projectile
            if (collisionsAster != -1): # if there is a collision
                self.Asteroids.listOfAsteroids += self.Asteroids.listOfAsteroids[collisionsAster].destroy() #destroy both the asteroid and the projectile.
                i.destroy()
