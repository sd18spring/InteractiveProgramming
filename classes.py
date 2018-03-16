import pygame
from math import cos,sin,sqrt,radians,atan,pi
import random
pygame.init()

class GUI():
    WHITE = (255,255,255)
    font = pygame.font.SysFont("couriernew",32)
    bx = 700
    by = 100

    def __init__(self,gD):
        self.gD = gD

    def update(self,ship):
        box = pygame.surface.Surface((self.bx, self.by))
        txt_surf = self.font.render(str(ship.score), True, self.WHITE)  # bottom line
        txt_rect = txt_surf.get_rect(center=(75, 40))
        box.blit(txt_surf, txt_rect)
        w,h = ship.oImage.get_size()
        txt_surf = pygame.transform.scale(ship.oImage,(int(w*.5),int(h*.5)))
        for x in range(ship.lives):
            spacing = x*45
            txt_rect = txt_surf.get_rect(center=(75-45+spacing, 90))
            box.blit(txt_surf, txt_rect)
        self.gD.blit(box,(0,0))

    def gameOver(self,ship):
        box = pygame.surface.Surface((300,500))
        gO = self.font.render("GAME OVER", True,self.WHITE)
        gO_rect = gO.get_rect(center=(90,90))
        box.blit(gO,gO_rect)
        txt_surf = self.font.render(str(ship.score), True, self.WHITE)  # bottom line
        txt_rect = txt_surf.get_rect(center=(90, 200))
        box.blit(txt_surf,txt_rect)
        w,h = self.gD.get_size()
        self.gD.blit(box,(int(w/2)-90,int(h/2)-90-40))


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
        self.startingAngle = angle
        self.angle = angle
        self.startingX = x
        self.startingY = y
        self.x = x
        self.y = y
        self.oImage = img
        self.nImage = img
        self.w,self.h = img.get_size()
        self.gD = gD
        self.rect = img.get_rect()
        self.changex = self.rect.w / 2
        self.changey = self.rect.h / 2
        self.rect.inflate_ip(-self.changex,-self.changey)
        self.rect.center = (self.x,self.y)
        self.score = 0
        self.lives = 3
        self.destroyed = False
        self.extraLives = 1
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
        self.changex = self.rect.w / 2
        self.changey = self.rect.h / 2
        self.rect.inflate_ip(-self.changex,-self.changey)
        self.rect.center = (self.x,self.y)
        self.angle -= posNeg*3

    def update(self):
        """MAGIC
        Does magic and makes the ship work.
        Updates position
        """
        if(self.score > 10000 * self.extraLives):
            self.lives += 1
            self.extraLives += 1
        if(self.destroyed):
            self.counter += 1
            if(self.counter == 120):
                self.destroyed = False
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
        #self.nImage.center = (self.x,self.y)
        #pygame.draw.rect(self.gD,(255,0,255),self.rect) # display's the ship's hit box in purple (for testing
        self.gD.blit(self.nImage,(self.rect.x - self.changex / 2, self.rect.y - self.changey / 2))
        #pygame.draw.rect(self.gD,(255,0,255),self.rect) # display's the ship's hit box in purple (for testing)
    def shoot(self,AllThings):
        x = self.x + int(5 * cos(self.angle))
        y = self.y + int(5 * sin(self.angle))
        AllThings.Projectiles.addProjectile(x,y,radians(self.angle),"Ship")
    def destroy(self):
        self.destroyed = True
        self.lives = self.lives - 1 # right now just a test, need to put something else here
        self.x = self.startingX
        self.y = self.startingY
        self.angle = self.startingAngle
        self.rotate(0)
        self.x_speed = 0
        self.y_speed = 0
        self.counter = 0
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
            self.x = self.x + (self.speed * cos(self.direction))  # Sets the Asteroid's to a small change in space
            self.y = self.y + (self.speed * sin(self.direction))
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
        self.type = "Large"
    def destroy(self):
        """
        destroys the asteroid and returns the asteroids that should take it's place.
        """
        if(not self.destroyed):
            self.destroyed = True
            MedAster = []
            for i in range(2):
                MedAster.append(MediumAsteroid(self.x,self.y,self.speed*1.5,random.uniform(0,2*pi),self.gameDisplay)) #makes two more medium asteroids in it's place with random directions
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
        self.type = "Medium"
    def destroy(self):
        """
        destroys the asteroid and returns the asteroids that should take it's place.
        """
        if(not self.destroyed):
            self.destroyed = True
            SmallAster = []
            for i in range(2):
                SmallAster.append(SmallAsteroid(self.x,self.y,self.speed*1.5,random.uniform(0,2*pi),self.gameDisplay)) #makes two more small asteroids in it's place with random directions
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
        self.type = "Small"
    def destroy(self):
        """
        destroys the asteroid and returns nothing because it is the smallest asteroid
        """
        self.destroyed = True
        return []
class CollectionOfAsteroids():
    """
    A collection of the Asteroids in the game
    listOfAsteroids - a list of the asteroids in the game
    listOfRects - a list of the hitboxes of the asteroids
    gameDisplay - the display
    """
    def __init__(self,gameDisplay):
        self.listOfAsteroids = []
        self.gameDisplay = gameDisplay
        self.speed = 1
    def spawnAsteroids(self,numberOfAsteroids):
        """
        spawns a set number of asteroids in the sides of the game
        """
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
            direction = random.uniform(0,pi * 2) # initiate each asteroid with a random direction
            listOfAsteroids.append(LargeAsteroid(x,y,self.speed,direction,self.gameDisplay))
            listOfRects.append(listOfAsteroids[i].rect)
        self.listOfAsteroids = listOfAsteroids
        self.listOfRects = listOfRects
    def update(self):
        """
        updates all the asteroids, deleting them from the list if they are destroyed.
        """
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
    def destroyAll(self):
        """
        function for testingasteroid, not for the real game
        """
        sizeOfAsteroids = range(len(self.listOfAsteroids))
        for i in sizeOfAsteroids:
            newAsteroid = self.listOfAsteroids[i].destroy()
            if(newAsteroid != None):
                self.listOfAsteroids += newAsteroid # destroying all of the asteroids making them medium
        for i in sizeOfAsteroids:
            self.listOfAsteroids.pop(0)
class Projectile():
    """
    projectiles that fire and destroy asteroids, ufos and players.
    x - position x
    y - position y
    w, h - size of the projectiles
    speed - speed of the projectile
    direction- direction given to the projectiles
    rect - the hitbox of the projectile
    gameDisplay - the display
    destroyed - senses whether the projectile is destroyed or not
    distanceTravelled - detects how far the projectile has travelled
    """
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
        width,height = self.gameDisplay.get_size()
        self.destroyed = False
        self.distanceTravelled = 0 # asteroids
        if(alliance == "Ship"):
            self.distanceWanted = 5/8 * height # the distance that the projectile travels before it is destroyed
        else:
            self.distanceWanted = 3/8 * height
        self.alliance = alliance
    def update(self):
        """
        updates the position of the particle
        """
        if(self.distanceTravelled < self.distanceWanted): # if the projectile has travelled farther than the wanted distance, it destroys itself
            width, height = self.gameDisplay.get_size() # gets the display's width and length
            self.x = self.x + (self.speed * cos(self.direction))  # Sets the speed to a small change in space
            self.y = self.y + (self.speed * sin(self.direction))
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
    """
    A collection of the Projectiles in the game
    listOfProjectiles - a list of the asteroids in the game
    listOfRects - a list of the hitboxes
    gameDisplay - the display
    """
    def __init__(self,gameDisplay):
        self.listOfProjectiles = [] #initializes the asteroidprojectiles
        self.listOfRects = [] # initializes their hitboxes
        self.gameDisplay = gameDisplay
    def addProjectile(self,x,y,direction,alliance):
        """
        Adds a projectile to the game at the given x y and direction with an alliance of either "UFO" or "Ship"
        """
        self.listOfProjectiles.append(Projectile(x,y,direction,alliance,self.gameDisplay)) # The spacebar command should call this
                                            # with the x,y and directions of the ship (with an offset bc of the front of the ship and that the origin is top left)
    def update(self):
        """
        Updates all of the projectiles
        """
        ListToDelete = [] # initializes the indices of what to delete
        ListOfRects = []
        for i in range(len(self.listOfProjectiles)):
            if(self.listOfProjectiles[i].destroyed):
                ListToDelete.append(i) # adding the index of destroyed particles to delete
            else:
                self.listOfProjectiles[i].update()
                ListOfRects.append(self.listOfProjectiles[i].rect)
        for j in reversed(ListToDelete):
            del self.listOfProjectiles[j]
        self.listOfRects = ListOfRects
class UFO():
    """
    A class of the general UFO, that moves autonomously and shoots
    (we didn't have enough time to implement a second UFO, so there is only one type of UFO)
    x - x position
    y - y position
    speed - speed of the ufo, constant
    destroyed - whether the UFO is destroyed or not
    image - the UFO image
    w,h - the height and width of the image
    FacingRight - the direction the UFO is facing(UFO goes either right to left or left to right)(also determines x position)
    counter - for recording the refractory period of the shooting
    listOfProjectiles - to allow it to call the add projectile function
    straight - whether the UFO goes straight across the screen or down then up
    """
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
        """
        updates the position of the UFO, as well as deciding when to shoot
        """
        if(self.counter % self.fireRate == 0):
            self.shoot()
        self.counter += 1
        width, height = self.gameDisplay.get_size()
        if(self.straight == True): # sometimes it goes straight accross, sometimes down then up
            if(self.FacingRight):
                self.direction = 0
            else:
                self.direction = pi
        else:
            if(self.FacingRight): # algorithm for going down then up
                if((self.x + self.w / 2) < width * 1 / 4):
                    self.direction = 0
                elif(self.x + self.w / 2 < width / 2):
                    self.direction = pi / 4
                else:
                    self.direction = - pi / 4
            else:
                if((self.x + self.w / 2) > width * 3 / 4):
                    self.direction = pi
                elif(self.x + self.w / 2 > width / 2):
                    self.direction = 5 * pi / 4
                else:
                    self.direction = 3 * pi / 4
        self.x = self.x + (self.speed * cos(self.direction))  # Sets the speed to a small change in space
        self.y = self.y + (self.speed * sin(self.direction))
        if(self.x >= width and self.FacingRight): # if the UFO goes out of the screen, destroy it
            self.destroyed = True
        elif(self.x <= 0 - self.w and not self.FacingRight):
            self.destroyed = True
        if(self.y >= height): # If the UFOs coordinate goes outside of the window, set that coordinate to the other side of the map
            self.y = 0 - self.h # adding the width of the image to make sure that the image doesn't appear suddenly (the image's position is the top right of the image)
        elif(self.y <= 0 - self.h): # same as above (makes it so that the whole image has to leave the screen for it to go to the other side)
            self.y = height
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
        #pygame.draw.rect(self.gameDisplay,(0,0,255),self.rect) # display's the UFO's hit box in blue (for testing)
        self.gameDisplay.blit(self.image,(self.x,self.y))
    def destroy(self):
        """
        destroys the UFO
        """
        self.destroyed = True
class BigUFO(UFO):
    """
    A subclass of UFO that shoots in a random direction and moves either straight or down then up
    shrinkage - how much to shrink the UFO image
    fireRate - cooldown for how often the UFO fires
    """
    def __init__(self,y,FacingRight,gameDisplay,listOfProjectiles):
        super().__init__(y,FacingRight,gameDisplay,listOfProjectiles)
        self.image = pygame.transform.scale(self.image,(self.w // 2,self.h // 2))
        self.w,self.h = self.image.get_size()
        self.shrinkage = 30
        self.rect = pygame.Rect((self.x + self.shrinkage / 2,self.y + self.shrinkage / 2),(self.w - self.shrinkage,self.h - self.shrinkage))
        self.fireRate = 60
    def shoot(self):
        """
        shoots a projectile
        """
        if(not self.destroyed):
            self.listOfProjectiles.addProjectile(self.x + self.w / 2,self.y + self.h / 2,random.uniform(0,2*pi),"UFO")
class CollectionOfUFOs():
    """
    A collection of the UFOs on the screen(there can only be one UFO, but this allows for an opportunity to add more if the game is too easy)
    listOfUFOs - the list of the UFOs on screen
    listOfRects - the list of the hitboxes of UFOs
    gameDisplay - display
    listOfProjectiles - the list of projectiles on screen so UFOs can shoot
    """
    def __init__(self,gameDisplay,listOfProjectiles):
        self.listOfUFOs = [] #initializes the projectiles
        self.listOfRects = [] # initializes their hitboxes
        self.gameDisplay = gameDisplay
        self.listOfProjectiles = listOfProjectiles
    def spawnBigUFO(self):
        """
        Spawns a big UFO in the game (would have been complemented by a spawnSmallUFO if time alloted)
        """
        width, height = self.gameDisplay.get_size()
        sampleUFO = BigUFO(0,True,self.gameDisplay,self.listOfProjectiles)
        y = random.randint(-sampleUFO.h // 2,height - sampleUFO.h // 2)
        facingRight = bool(random.getrandbits(1))
        self.listOfUFOs.append(BigUFO(y,facingRight,self.gameDisplay,self.listOfProjectiles))
    def update(self):
        """
        updates the list of UFOs
        """
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
    """
    List of all objects in the game:
    gameDisplay - display
    Asteroids - the collection of Asteroids
    Projectiles - the collection of Projectiles
    UFOs - the collection of UFOs
    ship - the ship in the game
    """
    def __init__(self,gameDisplay, ship):
        self.gameDisplay = gameDisplay
        self.Asteroids = CollectionOfAsteroids(gameDisplay)
        self.Projectiles = CollectionOfProjectiles(gameDisplay) # contains the CollectionOfAsteroids and CollectionOfProjectiles objects
        self.UFOs = CollectionOfUFOs(gameDisplay,self.Projectiles)
        self.ship = ship
    def update(self):
        """
        updates all objects and handles any collinion detection between objects
        """
        self.Asteroids.update()
        self.UFOs.update()
        self.Projectiles.update()
        collisionsAster = self.ship.rect.collidelist(self.Asteroids.listOfRects) # detects if any of the asteroids are in contact with the projectile
        if (collisionsAster != -1 and self.ship.destroyed == False): # if there is a collision
            self.Asteroids.listOfAsteroids += self.Asteroids.listOfAsteroids[collisionsAster].destroy() #destroy both the asteroid and the projectile.
            self.ship.destroy()
        collisionsUFO = self.ship.rect.collidelist(self.UFOs.listOfRects)
        if (collisionsUFO != -1 and self.ship.destroyed == False): # if there is a collision
            #self.UFOs.listOfUFOs[collisionsUFO].destroy() #destroy both the asteroid and the projectile.
            self.ship.destroy()
        collisionsProj = self.ship.rect.collidelist(self.Projectiles.listOfRects)
        if (collisionsProj != -1 and self.Projectiles.listOfProjectiles[collisionsProj].alliance != "Ship" and self.ship.destroyed == False):
            self.Projectiles.listOfProjectiles[collisionsProj].destroy()
            self.ship.destroy()
        for i in self.Projectiles.listOfProjectiles: # runs through each projectile
            collisionsAster = i.rect.collidelist(self.Asteroids.listOfRects) # detects if any of the asteroids are in contact with the projectile
            if (collisionsAster != -1): # if there is a collision
                if(i.alliance == "Ship"):
                    if(self.Asteroids.listOfAsteroids[collisionsAster].type == "Large"):
                        self.ship.score += 20
                    elif(self.Asteroids.listOfAsteroids[collisionsAster].type == "Medium"):
                        self.ship.score += 50
                    elif(self.Asteroids.listOfAsteroids[collisionsAster].type == "Small"):
                        self.ship.score += 100
                self.Asteroids.listOfAsteroids += self.Asteroids.listOfAsteroids[collisionsAster].destroy() #destroy both the asteroid and the projectile.
                i.destroy()
            collisionsUFO = i.rect.collidelist(self.UFOs.listOfRects)
            if (collisionsUFO != -1 and i.alliance != "UFO"): # if there is a collision
                self.UFOs.listOfUFOs[collisionsUFO].destroy() #destroy both the asteroid and the projectile.
                i.destroy()
                self.ship.score += 500
        for i in self.UFOs.listOfUFOs:
            collisionsAster = i.rect.collidelist(self.Asteroids.listOfRects) # detects if any of the asteroids are in contact with the projectile
            if (collisionsAster != -1): # if there is a collision
                self.Asteroids.listOfAsteroids += self.Asteroids.listOfAsteroids[collisionsAster].destroy() #destroy both the asteroid and the projectile.
                i.destroy()
