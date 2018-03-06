import character
class Model:
    def __init__(self, *args):
        self.g = -10
    def gravity(self, game_object):
        game_object.yvel += self.g
