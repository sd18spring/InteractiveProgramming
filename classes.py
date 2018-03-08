import pygame
import time
import math


class Model(object):

    def __init__(self, size):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.nodes = []
        self.nodes.append(Node('title',size[0]/2,size[1]/2))
        self.nodes.append(Node('title2',15,30))
        self.clines = []
        self.clines.append(ConnectionLine(self.nodes[0],self.nodes[1]))
        self.panning = False
        self.mouse_pos = None


    def zoom_in(self,center):
        """Zooms in around the center
        center: tuple containing the center about which the screen will
        be dilated"""
        for node in self.nodes:
            node.x = (node.x - center[0]/2)*1.05 + center[0]/2
            node.y = (node.y - center[1]/2)*1.05 + center[1]/2
        for cline in self.clines:
            cline.update()

    def zoom_out(self,center):
        """Zooms out around the center
        center: tuple containing the center about which the screen will
        be dilated"""
        for node in self.nodes:
            node.x = (node.x - center[0]/2)*0.95 + center[0]/2
            node.y = (node.y - center[1]/2)*0.95 + center[1]/2
        for cline in self.clines:
            cline.update()

    def pan(self,dx,dy):
        """Moves everything on the screen by dx,dy
        dx: movement in the x direction
        dy: movement in the y direction"""
        for node in self.nodes:
            node.x = node.x + dx
            node.y = node.y + dy
        for cline in self.clines:
            cline.update()


class Viewer(object):
    """Displays the model"""

    def __init__(self,model):
        self.model = model
        self.screen = pygame.display.set_mode(self.model.size)

    def draw(self):
        self.screen.fill(pygame.Color(63,63,63))
        for cline in self.model.clines:
            pygame.draw.lines(self.screen, pygame.Color(0,0,0), False, cline.points,
                        ConnectionLine.line_width)
        for node in self.model.nodes:
            pygame.draw.circle(self.screen, pygame.Color(127,127,63),
                            (int(node.x), int(node.y)), node.size,0)

        pygame.display.update()

class Controler(object):
    """Handles user input into the model"""

    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """Updates model according to type of input"""
        if model.panning:
            dx = pygame.mouse.get_pos()[0] - self.model.mouse_pos[0]
            dy = pygame.mouse.get_pos()[1] - self.model.mouse_pos[1]
            self.model.pan(dx,dy)
            self.model.mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                m_pos = pygame.mouse.get_pos()
                self.model.zoom_in(m_pos)

            elif event.button == 4:
                m_pos = pygame.mouse.get_pos()
                self.model.zoom_out(m_pos)

        if pygame.mouse.get_pressed()[0]:
            self.model.panning = True
            self.model.mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] == False:
            self.model.panning = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.model.pan(0,10)

            if event.key == pygame.K_DOWN:
                self.model.pan(0,-10)

            if event.key == pygame.K_LEFT:
                self.model.pan(10,-0)

            if event.key == pygame.K_RIGHT:
                self.model.pan(-10,0)



class Node(object):
    """A clickable node appearing in a web
    Attributes: x, y, title, children (list of the titles of nodes linked to
    by the node)"""

    node_size = 10

    def __init__(self,title,x,y):
        self.children = []
        self.x = x
        self.y = y
        self.title = title
        self.size = Node.node_size

    def __str__(self):
        return '%d,%d' % (self.x,self.y)


class ConnectionLine(object):

    line_length = 10
    line_width = 3

    def __init__(self,start,end):
        """Start and end are nodes"""
        self.start = start
        self.end = end
        self.x0 = start.x
        self.y0 = start.y
        self.x1 = end.x
        self.y1 = end.y
        self.points = [(self.x0,self.y0), (self.x1, self.y1)]

    def __str__(self):
        return 'Start: %s   End: %s'  % (str(self.start),str(self.end))

    def update(self):
        """Recalculates the line endpoints when nodes are changed"""
        self.x0 = self.start.x
        self.y0 = self.start.y
        self.x1 = self.end.x
        self.y1 = self.end.y
        self.points = [(self.x0,self.y0), (self.x1, self.y1)]



if __name__ == '__main__':

    pygame.init()

    node1 = Node('Node1',1,2)
    node2 = Node('Node2',3,4)



    running = True

    model = Model((1000,1000))


    view = Viewer(model)
    controler = Controler(model)
    #view.draw()
    k=0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            controler.handle_event(event)

            view.draw()
            time.sleep(.001)

    pygame.quit()
