import pygame
import time
import math as m
import wikipedia
from wiki_functions import summary_links
import webbrowser
import ast

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
        self.nodes.append(Node('',size[0]/2,size[1]/2))
        self.clines = [] #holds the connection lines of the model
        for i in range(1,len(self.nodes)):
            self.clines.append(ConnectionLine(self.nodes[0], self.nodes[-i]))
        self.panning = False #flag to tell if the model is currently panning
        self.mouse_pos = None
        self.boxes = [] #contians all the boxes in the model
        self.boxes.append(Box('Main Box'))
        self.rectangle = pygame.Rect(((size[0]/10),(size[1]/10),(size[0]/2),(size[1]/10)))
        self.scale = 1 #the current scale of the model, keeps track of zooming
        self.inputbox = Inputbox()
        self.inputboxes = []
        self.inputboxdisplay_list = []
        self.click_flag = False
        self.type_flag = False

    def __str__(self):
        node_list = []
        family_tree = {}
        cline_list = []

        for node in self.nodes:
            temp = []
            family_tree[node.title] = []
            temp.append(node.title)
            temp.append(node.x)
            temp.append(node.y)
            temp.append(node.level)
            temp.append(node.angle)
            temp.append(node.expanded)
            temp.append(node.links_viewed)
            temp.append(node.links)
            for child in node.children:
                i = self.nodes.index(child)
                family_tree[node.title].append(i)
            node_list.append(temp)

        for cline in self.clines:
            i_start = self.nodes.index(cline.start)
            i_end = self.nodes.index(cline.end)
            cline_list.append((i_start, i_end))
        return str(node_list) + '\n' + str(family_tree) + '\n' + str(cline_list)
        family_tree[node.title] = []

    def read_file(self,save_file):
        node_list = ast.literal_eval(save_file.readline())
        family_tree = ast.literal_eval(save_file.readline())
        cline_list = ast.literal_eval(save_file.readline())

        self.nodes = []
        self.clines = []

        for node in node_list:
            temp = Node(title = node[0], x = float(node[1]), y = float(node[2]), level = int(node[3]), angle = float(node[4]))
            temp.expanded = node[5]
            temp.links_viewed = node[6]
            temp.links = node[7]
            self.nodes.append(temp)

        for node in self.nodes:
            for child in family_tree[node.title]:
                node.children.append(self.nodes[child])

        for cline in cline_list:

            temp = ConnectionLine(self.nodes[cline[0]], self.nodes[cline[1]])
            self.clines.append(temp)



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
            node.update()
            if 0 <= node.x <= self.model.size[0]  and 0<= node.y <= self.model.size[1]:
                pygame.draw.circle(self.screen, pygame.Color(175,175,175),
                                (int(node.x),int(node.y)), node.size,0)

        for cline in self.model.clines: #use the length of each connection line to determine whether or not to draw a node title
            if 0 <= (cline.start.x <= self.model.size[0]  and 0<= cline.start.y <= self.model.size[1]) or (0 <= cline.end.x <= self.model.size[0]  and 0<= cline.end.y <= self.model.size[1]):
                if cline.length >=50: #this value changes the threshold for displaying text
                    self.screen.blit(cline.end.text_surface, (cline.end.x-15, cline.end.y-20))
        first_node = self.model.nodes[0]
        self.screen.blit(first_node.text_surface, (first_node.x-15, first_node.y+20))

        for box in self.model.boxes:
            pygame.draw.rect(self.screen,pygame.Color(225,225,225),pygame.Rect(((((self.model.width/2)-(self.model.width/4)),self.model.height/10,(self.model.width/2),(self.model.height/25)))))

        for lox in self.model.inputboxdisplay_list:
            pygame.draw.rect(self.screen,pygame.Color(200,200,200),pygame.Rect(((((self.model.width/2)-(self.model.width/4)),self.model.height/10,(self.model.width/2),(self.model.height/25)))))
            font1 = pygame.font.SysFont('Arial',32)
            text1 = font1.render('Search wikipedia...', True, (100,100,100))
            if len(self.model.inputbox.string) == 0:
                self.screen.blit(text1,(((self.model.width/2)-(self.model.width/4)),self.model.height/10))
            pass
        for zebox in self.model.inputboxes:
            font = pygame.font.SysFont('Arial',32)
            my_string = str(zebox.string)
            text = font.render(my_string, True, (50,50,50))
            self.screen.blit(text,(((self.model.width/2)-(self.model.width/4)),self.model.height/10))
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

            elif event.button == 3: #when right click is pressed, check if it is over a node and open in browser
                m_pos = pygame.mouse.get_pos()
                for node in self.model.nodes:
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size:
                        try:
                            page = wikipedia.page(node.title)
                            url = page.url
                        except:
                            url = 'https://en.wikipedia.org/wiki/Wikipedia:Disambiguation'
                        webbrowser.open(url, new=0, autoraise=True)
                        break



            elif event.button == 1: #case for left click
                m_pos = pygame.mouse.get_pos()
                for node in self.model.nodes: #check if the click is over a non-expanded node, if so, expand it
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size and not node.expanded and node.links:
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
                    self.model.click_flag = True
                    self.model.inputboxdisplay_list.append('yes')
                else:
                    self.model.click_flag = False
                    del self.model.inputboxdisplay_list[:]

        if pygame.mouse.get_pressed()[0]: #if the mouse is held down and not in the seach bar, turn on panning
            rect = self.model.rectangle
            m_pos = pygame.mouse.get_pos()
            if not (rect[0] < m_pos[0] < rect[0]+rect[2] and rect[1] < m_pos[1] < rect[1]+rect[3]):
                self.model.panning = True
                self.model.mouse_pos = pygame.mouse.get_pos() #update model mouse_pos

        elif pygame.mouse.get_pressed()[0] == False:
            self.model.panning = False


        if event.type == pygame.KEYDOWN:
            if self.model.click_flag == True:
                if event.key == pygame.K_a:
                    self.model.inputbox.string += 'a'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_b:
                    self.model.inputbox.string += 'b'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_c:
                    self.model.inputbox.string += 'c'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_d:
                    self.model.inputbox.string += 'd'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_e:
                    self.model.inputbox.string += 'e'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_f:
                    self.model.inputbox.string += 'f'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_g:
                    self.model.inputbox.string += 'g'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_h:
                    self.model.inputbox.string += 'h'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_i:
                    self.model.inputbox.string += 'i'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_j:
                    self.model.inputbox.string += 'j'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_k:
                    self.model.inputbox.string += 'k'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_l:
                    self.model.inputbox.string += 'l'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_m:
                    self.model.inputbox.string += 'm'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_n:
                    self.model.inputbox.string += 'n'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_o:
                    self.model.inputbox.string += 'o'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_p:
                    self.model.inputbox.string += 'p'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_q:
                    self.model.inputbox.string += 'q'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_r:
                    self.model.inputbox.string += 'r'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_s:
                    self.model.inputbox.string += 's'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_t:
                    self.model.inputbox.string += 't'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_u:
                    self.model.inputbox.string += 'u'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_v:
                    self.model.inputbox.string += 'v'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_w:
                    self.model.inputbox.string += 'w'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_x:
                    self.model.inputbox.string += 'x'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_y:
                    self.model.inputbox.string += 'y'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_z:
                    self.model.inputbox.string += 'z'
                    self.model.inputboxes.append(self.model.inputbox)

                if event.key == pygame.K_BACKSPACE:
                    self.model.inputbox.string = self.model.inputbox.string[:len(self.model.inputbox.string)-1]
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_TAB:
                    del self.model.inputboxdisplay_list[:]
                if event.key == pygame.K_CLEAR:
                    del self.model.inputboxes[:]
                    self.model.inputbox.string = ''
                if event.key == pygame.K_RETURN:
                    if '.txt' in self.model.inputbox.string:
                        try:
                            input_file = open('saved_trees/'+self.model.inputbox.string)
                            self.model.read_file(input_file)
                        except:
                            self.model.inputbox.string = ''
                    else:
                        new_stuff = self.model.delete_branch(0)
                        self.model.nodes = new_stuff[0] #give model a new list not containing the "deleted" nodes
                        self.model.clines = new_stuff[1]
                        self.model.nodes[0].title = self.model.inputbox.string
                        self.model.nodes[0].x = self.model.size[0]/2
                        self.model.nodes[0].y = self.model.size[1]/2
                        self.model.inputbox.string = ''
                        flag = summary_links(self.model.nodes[0].title)

                        self.model.nodes[0].links = flag
                        self.model.nodes[0].update()
                if event.key == pygame.K_ESCAPE:
                    del self.model.inputboxdisplay_list[:]
                if event.key == pygame.K_SPACE:
                    self.model.inputbox.string += ' '

                if event.key == pygame.K_EXCLAIM:
                    self.model.inputbox.string += '!'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_QUOTEDBL:
                    self.model.inputbox.string += '"'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_HASH:
                    self.model.inputbox.string += '#'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_DOLLAR:
                    self.model.inputbox.string += '$'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_AMPERSAND:
                    self.model.inputbox.string += '&'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_QUOTE:
                    self.model.inputbox.string += "'"
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_LEFTPAREN:
                    self.model.inputbox.string += '('
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_RIGHTPAREN:
                    self.model.inputbox.string += ')'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_ASTERISK:
                    self.model.inputbox.string += '*'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_PLUS:
                    self.model.inputbox.string += '+'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_COMMA:
                    self.model.inputbox.string += ','
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_MINUS:
                    self.model.inputbox.string += '-'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_PERIOD:
                    self.model.inputbox.string += '.'
                    self.model.inputboxes.append(self.model.inputbox)
                if event.key == pygame.K_SLASH:
                    self.model.inputbox.string += '/'
                    self.model.inputboxes.append(self.model.inputbox)
            elif event.key == pygame.K_d: #if d is pressed, expand every unexpanded node
                self.model.dive(1)
            elif event.key == pygame.K_1: #number keys set the model's n value
                self.model.n = 1
            elif event.key == pygame.K_2:
                self.model.n = 2
            elif event.key == pygame.K_3:
                self.model.n = 3
            elif event.key == pygame.K_4:
                self.model.n = 4
            elif event.key == pygame.K_5:
                self.model.n = 5
            elif event.key == pygame.K_6:
                self.model.n = 6
            elif event.key == pygame.K_7:
                self.model.n = 7
            elif event.key == pygame.K_8:
                self.model.n = 8
            elif event.key == pygame.K_9:
                self.model.n = 9
            elif event.key == pygame.K_DELETE:
                m_pos = pygame.mouse.get_pos()
                for node in self.model.nodes:
                    if ((m_pos[0]-node.x)**2+(m_pos[1]-node.y)**2)**.5 <= Node.node_size:
                        new_stuff = self.model.delete_branch(self.model.nodes.index(node))
                        self.model.nodes = new_stuff[0] #give model a new list not containing the "deleted" nodes
                        self.model.clines = new_stuff[1]
            elif event.key == pygame.K_s:
                save_file = open('saved_trees/' + self.model.nodes[0].title + '.txt', 'w')
                save_file.write(str(model))
class Inputbox(object):
    def __init__(self,string=''):
        self.string = string

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
    node_font = pygame.font.SysFont('Arial', 16)

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
        self.links_viewed = 0 #number of times the node has been expanded (after deletion of its children)
        self.links = []


    def __str__(self):
        return '%d,%d' % (self.x,self.y)

    def update(self):
        self.text_surface = Node.node_font.render(self.title, False, (0,0,0))


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
        #for theta in thetas:
        for theta in thetas:

            link = self.links[thetas.index(theta) + self.links_viewed]
            temp = Node(link,self.x + r*m.cos(m.radians(theta)), self.y - r*m.sin(m.radians(theta)), self.level + 1, theta)
            flag = summary_links(temp.title)

            temp.links = flag

            new_nodes.append(temp)
            self.children.append(temp)

        self.expanded = True
        self.links_viewed += n
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
            for i in range(n-2): #produces the angles of the new nodes
                angle = thetas[-1] + segment_angle
                if not(179 < abs(angle-self.angle) < 181): #exact comparison breaks down at some point, so I used an inequality
                    thetas.append(angle)
                else:
                    thetas.append(angle + segment_angle)

        else: #case for odd n values
            thetas.append(self.angle + segment_angle/2)
            for i in range(n-2): #produces the angles of the new nodes
                angle = thetas[-1] + segment_angle
                if not(179 < abs(angle-self.angle) < 181):
                    thetas.append(angle)
                else:
                    thetas.append(angle + segment_angle)

        count = 0
        for theta in thetas: #produces new nodes
            count += 1
            link = self.links[thetas.index(theta) + self.links_viewed % len(self.links)]
            temp = Node(link,self.x + r*m.cos(m.radians(theta)), self.y - r*m.sin(m.radians(theta)), self.level + 1, theta)
            temp.links = summary_links(temp.title)
            new_nodes.append(temp)
            self.children.append(temp)

        self.expanded = True
        self.links_viewed += n - 1
        return new_nodes

    def recursive_del(self, first = True):
        """Changes the attribute 'deleted' to true in the children and children's
        children of a node"""
        if not first:
            self.deleted = True
        self.expanded = False
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
        """Makes a line connecting (and acting as a pointer towards) two node objects"""
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
    node1 = Node('Node1',1,2)
    node2 = Node('Node2',3,4)
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
