import pygame
class Terrain:
    def __init__(self, pos, size = (100,100), kind = "Ground"):
        """
        Kind signifies the type of terrain (used for color and skins later)
        Each object is one terrain "block", with a 100x100 default size
        """
        self.pos = pos
        self.size = size
        self.kind = kind
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
