#This will be the boundary in which our snake navigates

class Boundary(object):
    """
    Defines a boundary object to confine the snake

    Takes attributes height, width, padding
    padding refers to wall thickness
    """

    def __init__(self, height, width, padding = 50):
        self.height = height
        self.width = width
        self.padding = padding
