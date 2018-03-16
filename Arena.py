#This will be the boundary in which our snake navigates

class Arena(object):
    """
    Defines a boundary object to confine the snake

    Takes attributes height, width, padding
    padding refers to wall thickness
    """

    def __init__(self, width=640, height=800, padding = 20):
        self.height = height
        self.width = width
        self.x = 0
        self.y = 0
        self.padding = padding

    def __str__(self):
        return "The Boundary is %f by %f and is %f units thick" % (self.height, self.width, self.padding)
