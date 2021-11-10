
class Corner(object):
        def __init__(self, right = -1, left = -1, forward = -1, orientation = 0):
                self.x = 0
                self.y = 0
                self.position = -1
                self.Left = None 
                self.Right = None
                self.Up = None
                self.Down = None         
                self.tremauxCounter = {0:0, 1:0, 2:0, 3:0}
                self.orientation = orientation
                if(orientation == 0):
                        self.distance = {0:forward, 1:right, 2:0, 3:left}
                elif(orientation == 1):
                        self.distance = {0:left, 1:forward, 2:right, 3:0}
                elif(orientation == 2):
                        self.distance = {0:0, 1:left, 2:forward, 3:right}
                else:
                        self.distance = {0:right, 1:0, 2:left, 3:forward}

        def Choose(self, orientation):
                if(orientation == 0):
                        direction = {0:"forward", 1:"right", 2:"backward", 3:"left"}
                elif(orientation == 1):
                        direction = {0:"left", 1:"forward", 2:"right", 3:"backward"}  
                elif(orientation == 2):
                        direction = {0:"backward", 1:"left", 2:"forward", 3:"right"}   
                else:
                        direction = {0:"right", 1:"backward", 2:"left", 3:"forward"} 

                backward = orientation + 2
                if(backward > 3):
                        backward -= 4
                self.tremauxCounter[backward] += 1
                
                wallFollowerDirection = {0:"right", 1:"forward", 2:"left"}
                for i in range (3): 
                        for j in range(4):
                                if(self.tremauxCounter[j] == 0 and self.distance[j]>-1 and wallFollowerDirection[i] == direction[j]):
                                        self.tremauxCounter[j]+=1
                                        return direction[j]
                    
                if(self.tremauxCounter[backward] == 1 and self.distance[backward]>-1):
                        self.tremauxCounter[backward]+=1
                        return direction[backward]

                for i in range (3): 
                        for j in range(4):
                                if(self.tremauxCounter[j] == 1 and self.distance[j]>-1 and wallFollowerDirection[i] == direction[j]):
                                        self.tremauxCounter[j]+=1
                                        return direction[j]
                
        def SetDistance(self, distance, orientation, prev):
                backward = orientation + 2
                if(backward > 3):
                        backward -= 4
                self.distance[backward] = distance
                prev.distance[orientation] = distance

        def SetPoint(self, prev, orientation):
                if(orientation == 0):
                        prev.Up = self
                        self.Down = prev
                elif(orientation == 1):
                        prev.Right = self
                        self.Left = prev
                elif(orientation == 2):
                        prev.Down = self
                        self.Up = prev
                else:
                        prev.Left = self
                        self.Right = prev

        def GetPoint(self, orientation):
                if(orientation == 0):
                        return self.Up
                elif(orientation == 1):
                        return self.Right
                elif(orientation == 2):
                        return self.Down
                elif(orientation == 3):
                        return self.Left
                else:
                        return None

        def GetDirection(self, orientation, corner):
                if(orientation == 0):
                        if(corner == self.Up):
                                return "Forward"
                        elif(corner == self.Right):
                                return "Right"
                        elif(corner == self.Left):
                                return "Left"
                elif(orientation == 1):
                        if(corner == self.Right):
                                return "Forward"
                        elif(corner == self.Down):
                                return "Right"
                        elif(corner == self.Up):
                                return "Left"
                elif(orientation == 2):
                        if(corner == self.Down):
                                return "Forward"
                        elif(corner == self.Left):
                                return "Right"
                        elif(corner == self.Right):
                                return "Left"
                else:
                        if(corner == self.Left):
                                return "Forward"
                        elif(corner == self.Up):
                                return "Right"
                        elif(corner == self.Down):
                                return "Left"

        def SetPostion(self, positon):
                self.position = positon

