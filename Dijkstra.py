from Corner import Corner

class Node(object):
        def __init__(self, corner, distance, prev):
                self.corner = corner
                self.distance = distance
                self.prev = prev


class Nodes(object):
        def __init__(self):
                self.nodes = list()
                self.prevNode = None

        def AddNode(self, corner, distance = 0, prev = None):
                check = 1
                for node in self.nodes:
                        if(node.corner == corner):
                                if(distance < node.distance):
                                        node.distance = distance
                                        node.prev = prev
                                check = 0
                if(check):
                    self.nodes.append(Node(corner, distance, prev))

        def GetNextNode(self, node):
                if(node == None):
                        node = self.prevNode
                        node.distance = 99999
                distance = node.distance
                nextNode = node
                for n in self.nodes:
                        if(distance > n.distance and n.corner.position < 0):
                                distance = n.distance
                                nextNode = n
                self.prevNode = nextNode
                return nextNode

        def GetLastNode(self):
                return self.nodes.__getitem__(-1)

class Dijkstra(object):
        def __init__(self, start):
                self.start = start
                self.nodes = Nodes()
                self.nodes.AddNode(start)
                self.distance = 0

        def DijkstraAlgoritham(self):
                corner = self.start
                while(corner.position < 2):
                        node = self.ShortesDistance(corner)
                        node = self.nodes.GetNextNode(node)
                        self.distance = node.distance
                        corner = node.corner

        def ShortesDistance(self, corner):
                if(corner.position < 0):
                        corner.position = 0
                minDistance = 99999
                node = None
                for i in range(4):
                        nextCorner = corner.GetPoint(i)
                        if(nextCorner != None and (nextCorner.position < 0 or nextCorner.position == 2)):
                                distance = corner.distance[i]
                                if(distance > 0):
                                        self.nodes.AddNode(corner.GetPoint(i), distance + self.distance, corner)
                                        if(minDistance >= distance):
                                                minDistance = distance
                                                node = self.nodes.GetLastNode()

                return node

        def FindShortesPath(self):
                self.DijkstraAlgoritham()
                node = self.nodes.GetLastNode()
                corners = list()
                corner = node.corner
                while(node.prev != None):
                        for n in self.nodes.nodes:
                                if(n.corner == corner):
                                        corners.append(corner)
                                        corner = n.prev
                                        node = n
                                        break
                return corners

