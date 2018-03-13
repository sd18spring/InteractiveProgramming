import pygame
import time
import math
import pygame_textinput

class Model(object):

    def __init__(self, size, boxes=None):
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.nodes = []
        self.nodes.append(Node('title',size[0]/2,size[1]/2))
        self.clines = []

        self.panning = False
        self.mouse_pos = None
        self.boxes = []
        self.boxes.append(Box(('Main Box'),((size[0]/2)-(size[0]/4)),((size[1]*.33)-(size[1]/30)))),
        self.rectangle = pygame.Rect(((size[0]/2)-(size[0]/4),(size[1]*.33)-(size[1]/30),(size[0]/2),(size[1]/10)))
        self.scale = 1

        self.inputboxes = []
        self.inputboxes2 = []

    def zoom_in(self,center):
        """Zooms in around the center
        center: tuple containing the center about which the screen will
        be dilated"""
        for node in self.nodes:
            node.x = (node.x - center[0])*1.05 + center[0]
            node.y = (node.y - center[1])*1.05 + center[1]
        for cline in self.clines:
            cline.update()
        self.scale = self.scale * 1.05

    def zoom_out(self,center):
        """Zooms out around the center
        center: tuple containing the center about which the screen will
        be dilated"""
        for node in self.nodes:
            node.x = (node.x - center[0])*0.95 + center[0]
            node.y = (node.y - center[1])*0.95 + center[1]
        for cline in self.clines:
            cline.update()
        self.scale = self.scale * 0.95

    def pan(self,dx,dy):
        """Moves everything on the screen by dx,dy
        dx: movement in the x direction
        dy: movement in the y direction"""
        for node in self.nodes:
            node.x = node.x + dx
            node.y = node.y + dy
        for cline in self.clines:
            cline.update()

    def inputbox(self):
        inputboxes.append(jean)

class Viewer(object):
    """Displays the model"""

    def __init__(self,model):
        self.model = model
        self.screen = pygame.display.set_mode(self.model.size)

    def draw(self):
        self.screen.fill(pygame.Color(28, 172, 229))
        for cline in self.model.clines:
            pygame.draw.lines(self.screen, pygame.Color(200, 200, 200), False, cline.points,
                        ConnectionLine.line_width)
        for node in self.model.nodes:
            pygame.draw.circle(self.screen, pygame.Color(175,175,175),
                            (int(node.x), int(node.y)), node.size,0)
        for box in self.model.boxes:
            pygame.draw.rect(self.screen,pygame.Color(225,225,225),pygame.Rect(((self.model.width/2)-(self.model.width/4),(self.model.height*.33)-(self.model.height/30),(self.model.width/2),(self.model.height/10))))

        for zebox in self.model.inputboxes2:
            font = pygame.font.SysFont("arial", 20)
            textinput = pygame_textinput.TextInput()
            my_in = ''

            return_hit = False

            while return_hit != True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        return_hit = True

                if textinput.update(events):
                   my_in = textinput.get_text()
                   textinput = pygame_textinput.TextInput()

                self.screen.blit(textinput.get_surface(),(((self.model.width/2)-(self.model.width/4),(self.model.height*.33)-(self.model.height/30))))
                display = font.render(my_in, True, (100,100,100))
                self.screen.blit(display,(((self.model.width/2)-(self.model.width/4)),((self.model.height*.33)-(self.model.height/30))+30))
                pygame.display.update()
                time.sleep(.0001)

            return draw(self)
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
                rect = self.model.rectangle
                if rect[0] < m_pos[0] < rect[0]+rect[2] and rect[1] < m_pos[1] < rect[1]+rect[3]:
                    if len(self.model.inputboxes2) == 0:
                        self.model.inputboxes2.append(input_box())
                    else:
                        self.model.inputboxes2.clear()
                for node in self.model.nodes:
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size:
                        self.model.nodes.extend(node.expand(self.model.scale))
                        self.model.clines.append(ConnectionLine(node, self.model.nodes[-1]))
                        self.model.clines.append(ConnectionLine(node, self.model.nodes[-2]))
                        self.model.clines.append(ConnectionLine(node, self.model.nodes[-3]))

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

class Inputbox(object):

    def __init__(self,x,y):
        self.x = x
        self.y = y


class input_box(object):
    def __init__(self,x=0):
        self.x = x


class Box(object):
    """A clickable box where the user enters the title of the page she/he is
    interested in"""

    def __init__(self,title='',x=0,y=0):
        self.title = title
        self.x = x
        self.y = y

    def __str__(self):
        return '%s at (%d,%d)' % (title,x,y)

class Node(object):
    """A clickable node appearing in a web
    Attributes: x, y, title, children (list of the titles of nodes linked to
    by the node)"""

    node_size = 10

    def __init__(self,title,x,y, level = 1):
        self.children = []
        self.x = x
        self.y = y
        self.title = title
        self.size = Node.node_size
        self.level = level
        self.expanded = False

    def __str__(self):
        return '%d,%d' % (self.x,self.y)

    def expand(self, scale):
        r = 100*scale/1.2**(self.level)

        first = Node('1', self.x, self.y + r, self.level + 1)
        second = Node('2', self.x + r*math.sin(math.pi/3), self.y - r*math.cos(math.pi/3), self.level + 1)
        third = Node('3', self.x - r*math.sin(math.pi/3), self.y - r*math.cos(math.pi/3), self.level + 1)

        cline1 = ConnectionLine(self, first)
        cline2 = ConnectionLine(self, second)
        cline3 = ConnectionLine(self, third)

        return [first, second, third]

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
