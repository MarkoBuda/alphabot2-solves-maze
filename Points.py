from Corner import Corner
import math

class Point(object):
        def __init__(self, corner):
                self.x = corner.x
                self.y = corner.y
                self.corner = corner

class Points(object):
        def __init__(self):
                self.points = list()

        def CheckPoint(self, corner, distance, orientation):
                x = corner.x
                y = corner.y
                if(orientation == 0):
                        x = x+distance
                elif(orientation == 1):
                        y = y+distance
                elif(orientation == 2):
                        x = x-distance
                else:
                        y = y-distance
                for point in self.points:
                        if(math.sqrt(pow(point.x - x, 2) + pow(point.y - y, 2)) <250):
                                return point.corner

                return None

        def AddPoint(self, corner, distance, orientation, prev):
                if(orientation == 0):
                        corner.x = prev.x+distance
                        corner.y = prev.y
                elif(orientation == 1):
                        corner.x = prev.x
                        corner.y = prev.y+distance
                elif(orientation == 2):
                        corner.x = prev.x-distance
                        corner.y = prev.y
                else:
                        corner.x = prev.x
                        corner.y = prev.y-distance
                self.points.append(Point(corner))
