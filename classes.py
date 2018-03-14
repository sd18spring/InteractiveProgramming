import pygame
import time
import math as m

class Model(object):
    """Representation of all of the objects being displayed
    Attributes: size, width, height, nodes, n, clines, panning, mouse_pos, boxes,
    rectangle, scale"""

    def __init__(self, size, boxes=None):
        self.size = size #size of the window of the model
        self.width = size[0]
        self.height = size[1]
        self.nodes = [] #holds all of the nodes in the model
        self.n = 3 #1 + the number of new nodes produced with an expansion
        self.nodes.append(Node('title',size[0]/2,size[1]/2))
        self.nodes.extend(self.nodes[0].init_expand(1,self.n))
        self.clines = [] #holds the connection lines of the model
        for i in range(1,len(self.nodes)):
            self.clines.append(ConnectionLine(self.nodes[0], self.nodes[-i]))
        self.panning = False #flag to tell if the model is currently panning
        self.mouse_pos = None
        self.boxes = [] #contians all the boxes in the model
        self.boxes.append(Box('Main Box'))
        self.rectangle = pygame.Rect(((size[0]/2)-(size[0]/4),(size[1]*.33)-(size[1]/30),(size[0]/2),(size[1]/10)))
        self.scale = 1 #the current scale of the model, keeps track of zooming


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

    def delete_branch(self, node_index):
        """Returns a list of nodes and connection lines excluding the ones
        farther out on the tree of the node at self.nodes[node_index]"""

        self.nodes[node_index].recursive_del()

        new_nodes = [node for node in self.nodes if not node.deleted]
        new_clines = [cline for cline in self.clines if not (cline.start.deleted or cline.end.deleted)]

        return new_nodes, new_clines

class Viewer(object):
    """Displays the model
    Attributes: model, screen"""

    def __init__(self,model):
        self.model = model
        self.screen = pygame.display.set_mode(self.model.size)

    def draw(self):
        """Displays all the connecting lines, then the nodes, and finally the
        titles of each node"""
        self.screen.fill(pygame.Color(28, 172, 229))
        for cline in self.model.clines: #draw all of the connection lines, but only if they are one screen
            cline.update()
            if 0 <= (cline.start.x <= self.model.size[0]  and 0<= cline.start.y <= self.model.size[1]) or (0 <= cline.end.x <= self.model.size[0]  and 0<= cline.end.y <= self.model.size[1]):
                pygame.draw.lines(self.screen, pygame.Color(200, 200, 200), False, cline.points,
                            ConnectionLine.line_width)

        for node in self.model.nodes: #draw all of the nodes, but only if they are on screen
            if 0 <= node.x <= self.model.size[0]  and 0<= node.y <= self.model.size[1]:
                pygame.draw.circle(self.screen, pygame.Color(175,175,175),
                                (int(node.x),int(node.y)), node.size,0)

        for cline in self.model.clines: #use the length of each connection line to determine whether or not to draw a node title
            if 0 <= (cline.start.x <= self.model.size[0]  and 0<= cline.start.y <= self.model.size[1]) or (0 <= cline.end.x <= self.model.size[0]  and 0<= cline.end.y <= self.model.size[1]):
                if cline.length >=50: #this value changes the threshold for displaying text
                    self.screen.blit(cline.end.text_surface, (cline.end.x-15, cline.end.y-20))
        first_node = self.model.nodes[0]
        self.screen.blit(first_node.text_surface, (first_node.x-15, first_node.y+20))
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


        if model.panning: #if currently panning, pan by the mouse movement since last check
            dx = pygame.mouse.get_pos()[0] - self.model.mouse_pos[0]
            dy = pygame.mouse.get_pos()[1] - self.model.mouse_pos[1]
            self.model.pan(dx,dy)
            self.model.mouse_pos = pygame.mouse.get_pos() #update mouse position

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 5: #zoom in with scroll up
                m_pos = pygame.mouse.get_pos()
                self.model.zoom_in(m_pos)

            elif event.button == 4: #zoom out with scroll down
                m_pos = pygame.mouse.get_pos()
                self.model.zoom_out(m_pos)

            elif event.button == 3: #when right click is pressed, check if it is over a node
                m_pos = pygame.mouse.get_pos()
                for node in self.model.nodes:
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size:
                        new_stuff = self.model.delete_branch(self.model.nodes.index(node))
                        self.model.nodes = new_stuff[0] #give model a new list not containing the "deleted" nodes
                        self.model.clines = new_stuff[1]


            elif event.button == 1: #case for left click
                m_pos = pygame.mouse.get_pos()
                for node in self.model.nodes: #check if the click is over a non-expanded node, if so, expand it
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size and not node.expanded:
                        if self.model.nodes.index(node) == 0:
                            self.model.nodes.extend(node.init_expand(self.model.scale, self.model.n))
                            for i in range(self.model.n):
                                self.model.clines.append(ConnectionLine(node, self.model.nodes[-i-1]))
                            self.model.zoom_in((int(node.x),int(node.y)),(m.sqrt(5)+model.n-2)/2)
                            break
                        else:
                            self.model.nodes.extend(node.expand_n(self.model.scale, self.model.n))
                            for i in range(1,self.model.n):
                                self.model.clines.append(ConnectionLine(node, self.model.nodes[-i]))
                            self.model.zoom_in((int(node.x),int(node.y)),(m.sqrt(5)+model.n-2)/2)
                            break

                rect = self.model.rectangle

                if rect[0] < m_pos[0] < rect[0]+rect[2] and rect[1] < m_pos[1] < rect[1]+rect[3]:
                    print('yay!')
                print(self.model.mouse_pos)

        if pygame.mouse.get_pressed()[0]: #if the mouse is held down and not in the seach bar, turn on panning
            rect = self.model.rectangle
            m_pos = pygame.mouse.get_pos()
            if not (rect[0] < m_pos[0] < rect[0]+rect[2] and rect[1] < m_pos[1] < rect[1]+rect[3]):
                self.model.panning = True
                self.model.mouse_pos = pygame.mouse.get_pos() #update model mouse_pos

        elif pygame.mouse.get_pressed()[0] == False:
            self.model.panning = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d: #if d is pressed, expand every unexpanded node
                self.model.dive(1)
            if event.key == pygame.K_1: #number keys set the model's n value
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
            if event.key == pygame.K_8:
                self.model.n = 8
            if event.key == pygame.K_9:
                self.model.n = 9

class Box(object):
    """A clickable box where the user enters the title of the page she/he is
    interested in"""

    def __init__(self,title=''):
        self.title = title

    def __str__(self):
        return '%s at (%d,%d)' % (title,x,y)

class Node(object):
    """A clickable node appearing in a web, which produces more nodes (children)
    when clicked
    Attributes: x, y, title, size, level, expanded, angle, text_surface,
    children, deleted, times_refreshed"""
    pygame.font.init()
    node_size = 10
    node_font = pygame.font.SysFont('Arial', 13)

    def __init__(self,title,x,y, level = 1, angle = 0):
        self.children = [] #nodes created from the expansion of this node
        self.x = x
        self.y = y
        self.title = title #title of the article linked to by the node
        self.size = Node.node_size
        self.level = level #how many clicks the node is away from the center
        self.expanded = False #whether the node has children
        self.angle = angle #angle from a horizontal line formed by the segemnt from this node's parent to it
        self.text_surface = Node.node_font.render(self.title, False, (0,0,0))
        self.deleted = False #flag for use in the removal of nodes from the model
        self.times_refreshed = 0 #number of times the node has been expanded (after deletion of its children)


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
                self.children.append(temp)

        self.expanded = True
        return new_nodes

    def expand_n(self,scale, n = 3):
        """Returns nodes such that they form a regular n-gon in a pattern which
        forms a non-intersecting fractal
        scale: float, scale factor of the Model
        n: number of sides of the polygon greated (n-1 new nodes are created)"""
        r = 100*scale/((m.sqrt(5)+ n - 2)/2)**(self.level) #formula to produce node distances such that clines are non-intersecting
        thetas = []
        new_nodes = []
        segment_angle = 360/n
        if n%2 == 0: #case for even n values
            thetas.append(self.angle)
            for i in range(n-1): #produces the angles of the new nodes
                angle = thetas[-1] + segment_angle
                if not(179 < abs(angle-self.angle) < 181):
                    thetas.append(angle)
                else:
                    thetas.append(angle + segment_angle)

        else: #case for odd n values
            thetas.append(self.angle + segment_angle/2)
            for i in range(n-1): #produces the angles of the new nodes
                angle = thetas[-1] + segment_angle
                if not(179 < abs(angle-self.angle) < 181):
                    thetas.append(angle)
                else:
                    thetas.append(angle + segment_angle)

        for theta in thetas: #produces new nodes
            temp = Node(str(theta),self.x + r*m.cos(m.radians(theta)), self.y - r*m.sin(m.radians(theta)), self.level + 1, theta)
            new_nodes.append(temp)
            self.children.append(temp)

        return new_nodes

    def recursive_del(self, first = True):
        """Changes the attribute 'deleted' to true in the children and children's
        children of a node"""
        if not first:
            self.deleted = True
        self.expanded = False
        self.times_refreshed += 1
        first = False
        if self.children == []:
            return
        for child in self.children:
            child.recursive_del(first)



class ConnectionLine(object):
    """A line connecting a node to each of it's children, the length being determined
    by the locations of the nodes within it
    Attributes: start, end, x0, x1, y0, y1, length, points"""
    line_width = 3

    def __init__(self,start,end):
        """Start and end are nodes"""
        self.start = start
        self.end = end
        self.x0 = start.x
        self.y0 = start.y
        self.x1 = end.x
        self.y1 = end.y
        self.length = m.sqrt((self.x1 - self.x0)**2 + (self.y1-self.y0)**2)
        self.points = [(self.x0,self.y0), (self.x1, self.y1)] #list containing end points as tuples

    def __str__(self):
        return 'Start: %s   End: %s'  % (str(self.start),str(self.end))

    def update(self):
        """Recalculates the line endpoints and length when nodes are changed"""
        self.x0 = self.start.x
        self.y0 = self.start.y
        self.x1 = self.end.x
        self.y1 = self.end.y
        self.length = m.sqrt((self.x1 - self.x0)**2 + (self.y1-self.y0)**2)
        self.points = [(self.x0,self.y0), (self.x1, self.y1)]

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()

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
