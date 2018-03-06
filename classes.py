class Node(object):

    node_size = 10

    def __init__(self,title,x,y):
        self.x = x
        self.y = y
        self.size = 10

    def __str__(self):
        return '%d,%d' % (self.x,self.y)


class ConnectionLine(object):

    line_length = 10

    def __init__(self,start,end):
        """Start and end are nodes"""
        self.start = start
        self.end = end
        self.x0 = start.x
        self.y0 = start.y
        self.x1 = end.x
        self.y1 = end.y

    def __str__(self):
        return 'Start: %s   End: %s'  % (str(self.start),str(self.end))

node1 = Node('Node1',1,2)
node2 = Node('Node2',3,4)
print(ConnectionLine(node1,node2))
