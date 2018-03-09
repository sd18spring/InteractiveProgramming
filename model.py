import character
import terrain
import random
class Model:
    def __init__(self, *args):
        self.g = -10
        self.terrains = []
        for i in range(10):
            for j in range(3):
                self.terrains.append(terrain.Terrain((i * 100,1000 - j * 100)))
        #for i in range(10):
        #    if(random.randint(1,2) == 2):
        #        self.terrains.append(terrain.Terrain((i * 100,1000 - 3 * 100)))
        self.char = character.Character(500, 600)
    def gravity(self, game_object):
        game_object.yvel += self.g
