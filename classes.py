import pygame
import time
import math as m

class Model(object):

    def __init__(self, size, boxes=None):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.nodes = []
        self.n = 3
        self.nodes.append(Node('title',size[0]/2,size[1]/2))
        self.nodes.extend(self.nodes[0].init_expand(1,self.n))
        self.clines = []
        for i in range(1,len(self.nodes)):
            self.clines.append(ConnectionLine(self.nodes[0], self.nodes[-i]))
        self.panning = False
        self.mouse_pos = None
        self.boxes = []
        self.boxes.append(Box('Main Box'))
        self.rectangle = pygame.Rect(((size[0]/2)-(size[0]/4),(size[1]*.33)-(size[1]/30),(size[0]/2),(size[1]/10)))
        self.scale = 1


    def zoom_in(self,center,scale = 1.05):
        """Zooms in around the center by a factor of scale
        center: tuple containing the center about which the screen will
        be dilated
        scale: value representing how far to zoom in"""
        for node in self.nodes:
            if node.x *scale >= 2**30 or node.y *scale >= 2**30:
                print('max depth reached')
                return
        for node in self.nodes:
            node.x = (node.x - center[0])*scale + center[0]
            node.y = (node.y - center[1])*scale + center[1]
        for cline in self.clines:
            cline.update()
        self.scale = self.scale * scale

    def zoom_out(self,center, scale = 0.95):
        """Zooms out around the center by a factor of scale
        center: tuple containing the center about which the screen will
        be dilated
        scale: float representing dilation"""

        for node in self.nodes:
            node.x = (node.x - center[0])*scale + center[0]
            node.y = (node.y - center[1])*scale + center[1]
        for cline in self.clines:
            cline.update()
        self.scale = self.scale * scale

    def pan(self,dx,dy):
        """Moves everything on the screen by dx,dy
        dx: movement in the x direction
        dy: movement in the y direction"""


        for node in self.nodes:
            node.x = node.x + dx
            node.y = node.y + dy
        for cline in self.clines:
            cline.update()

    def dive(self, depth):
        """Expands each node in the current model out to a fixed depth
        depth: int, determines how far the model evaluates new nodes"""
        for i in range(depth):
            for i in range(len(self.nodes)):
                node = self.nodes[i]
                if node.expanded == False:
                    self.nodes.extend(node.expand_n(self.scale, self.n))
                    for i in range(1, self.n):
                        self.clines.append(ConnectionLine(node, self.nodes[-i]))


class Viewer(object):
    """Displays the model"""

    def __init__(self,model):
        self.model = model
        self.screen = pygame.display.set_mode(self.model.size)

    def draw(self):
        self.screen.fill(pygame.Color(28, 172, 229))
        for cline in self.model.clines:
            cline.update()
            if 0 <= (cline.start.x <= self.model.size[0]  and 0<= cline.start.y <= self.model.size[1]) or (0 <= cline.end.x <= self.model.size[0]  and 0<= cline.end.y <= self.model.size[1]):
                pygame.draw.lines(self.screen, pygame.Color(200, 200, 200), False, cline.points,
                            ConnectionLine.line_width)
        for node in self.model.nodes:
            if 0 <= node.x <= self.model.size[0]  and 0<= node.y <= self.model.size[1]:
                pygame.draw.circle(self.screen, pygame.Color(175,175,175),
                                (int(node.x),int(node.y)), node.size,0)
        """for box in self.model.boxes:
            pygame.draw.rect(self.screen,pygame.Color(255,255,255),pygame.Rect(((self.model.width/2)-(self.model.width/4),(self.model.height*.33)-(self.model.height/30),(self.model.width/2),(self.model.height/10))))
"""
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

            elif event.button == 1:
                m_pos = pygame.mouse.get_pos()
                for node in self.model.nodes:
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size and node.expanded == False:
                        self.model.nodes.extend(node.expand_n(self.model.scale, self.model.n))
                        for i in range(1,self.model.n):
                            self.model.clines.append(ConnectionLine(node, self.model.nodes[-i]))
                        self.model.zoom_in((int(node.x),int(node.y)),(m.sqrt(5)+model.n-2)/2)
                        break

                rect = self.model.rectangle

                if rect[0] < m_pos[0] < rect[0]+rect[2] and rect[1] < m_pos[1] < rect[1]+rect[3]:
                    print('yay!')
                print(self.model.mouse_pos)

        if pygame.mouse.get_pressed()[0]:
            rect = self.model.rectangle
            m_pos = pygame.mouse.get_pos()
            if not (rect[0] < m_pos[0] < rect[0]+rect[2] and rect[1] < m_pos[1] < rect[1]+rect[3]):
                self.model.panning = True
                self.model.mouse_pos = pygame.mouse.get_pos()

        elif pygame.mouse.get_pressed()[0] == False:
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

            if event.key == pygame.K_d:
                self.model.dive(1)
            if event.key == pygame.K_1:
                self.model.n = 1
            if event.key == pygame.K_2:
                self.model.n = 2
            if event.key == pygame.K_3:
                self.model.n = 3
            if event.key == pygame.K_4:
                self.model.n = 4
            if event.key == pygame.K_5:
                self.model.n = 5
            if event.key == pygame.K_6:
                self.model.n = 6
            if event.key == pygame.K_7:
                self.model.n = 7


class Box(object):
    """A clickable box where the user enters the title of the page she/he is
    interested in"""

    def __init__(self,title=''):
        self.title = title

    def __str__(self):
        return '%s at (%d,%d)' % (title,x,y)

class Node(object):
    """A clickable node appearing in a web
    Attributes: x, y, title, size, level, expanded, angle"""

    node_size = 10

    def __init__(self,title,x,y, level = 1, angle = 0):
        self.children = []
        self.x = x
        self.y = y
        self.title = title
        self.size = Node.node_size
        self.level = level
        self.expanded = False
        self.angle = angle

    def __str__(self):
        return '%d,%d' % (self.x,self.y)

    def init_expand(self, scale  =1, n =3):
        """Produces n nodes surrouding self in a regular n-gon
        scale: float, the scale factor of the Model
        n: number of new nodes to make"""
        r = 100*scale
        segment_angle = 360/n
        new_nodes = []
        thetas = [90]
        for i in range(n-1):
            thetas.append(thetas[-1]+segment_angle)
        for theta in thetas:
            for theta in thetas:
                temp = Node(str(theta),self.x + r*m.cos(m.radians(theta)), self.y - r*m.sin(m.radians(theta)), self.level + 1, theta)
                new_nodes.append(temp)

        self.expanded = True
        return new_nodes

    def expand_n(self,scale, n = 3):
        """Produces nodes such that they form a regular n-gon in a pattern which
        forms a non-intersecting fractal
        scale: float, scale factor of the Model
        n: number of sides of the polygon greated (n-1 new nodes are created)"""
        r = 100*scale/((m.sqrt(5)+ n - 2)/2)**(self.level)
        thetas = []
        new_nodes = []
        segment_angle = 360/n
        if n%2 == 0:
            thetas.append(self.angle)
            for i in range(n-1):
                angle = thetas[-1] + segment_angle
                if abs(angle-self.angle) != 180:
                    thetas.append(angle)
                else:
                    thetas.append(angle + segment_angle)

        else:
            thetas.append(self.angle + segment_angle/2)
            for i in range(n-1):
                angle = thetas[-1] + segment_angle
                if abs(angle-self.angle) != 180:
                    thetas.append(angle)
                else:
                    thetas.append(angle + segment_angle)

        for theta in thetas:
            temp = Node(str(theta),self.x + r*m.cos(m.radians(theta)), self.y - r*m.sin(m.radians(theta)), self.level + 1, theta)
            new_nodes.append(temp)

        return new_nodes



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

    running = True

    model = Model((1000,1000))

    view = Viewer(model)
    controler = Controler(model)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            controler.handle_event(event)

            view.draw()
            time.sleep(.001)

    pygame.quit()
