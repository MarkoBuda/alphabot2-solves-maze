import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from TRSensors import TRSensor
from MazeMovement import MazeMovement
from Corner import Corner
import time
from Points import Points
from Dijkstra import Dijkstra

Button = 7
right = -1
left = -1
forward = -1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Button,GPIO.IN,GPIO.PUD_UP)

while (GPIO.input(Button) != 0):
        time.sleep(0.05)

TR = TRSensor()
Ab = AlphaBot2()
Movement = MazeMovement( Ab, TR, 25)
time.sleep(0.5)
Movement.Calibrate()
time.sleep(3)

while (GPIO.input(Button) != 0):
        time.sleep(0.05)

start = Corner()
start.SetPostion(1)
dijkstra = Dijkstra(start)
points = Points()
corner = start
distance = 0
direction = -1
orientation = 0
points.AddPoint(corner, distance, orientation, start)

while True:
        position,Sensors = TR.readLine()
        if(orientation > 3):
                orientation -= 4
        elif(orientation < 0):
                orientation +=4
        if(Sensors[0] <300 and Sensors[1] < 300 and Sensors[2] < 300 and Sensors[3] < 300 and Sensors[4] < 300 and
                Sensors[0] > 100 and Sensors[1] > 100 and Sensors[2] > 100 and Sensors[3] > 100 and Sensors[4] > 100):
                prev = corner
                corner = Corner(right, left, forward, orientation)
                points.AddPoint(corner, distance, orientation, prev)
                corner.SetDistance(distance, orientation, prev)
                corner.SetPoint(prev, orientation)
                corner.SetPostion(2)
                orientation+=2
                if(orientation > 3):
                        orientation -= 4
                elif(orientation < 0):
                        orientation +=4
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                time.sleep(0.5)
                Movement.Turn180()
                time.sleep(1)
                direction = ""
        if(right == 0 or left == 0 or forward == 0):
                check = points.CheckPoint(corner, distance, orientation)
                prev = corner
                if(check != None ):
                        corner = check
                        check = None
                        if(corner.position == 1):
                                Movement.Turn180()
                                orientation = 0
                                break
                else:
                        corner = Corner(right, left, forward, orientation)
                        points.AddPoint(corner, distance, orientation, prev)
                direction = corner.Choose(orientation)
                corner.SetDistance(distance, orientation, prev)
                corner.SetPoint(prev, orientation)
                right = -1
                left = -1
                forward = -1
        if(direction == "right"):
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                time.sleep(0.5)
                Movement.Right()
                direction = ""
                time.sleep(3)
                orientation +=1
        elif(direction == "forward"):
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                time.sleep(0.5)
                direction = ""
                time.sleep(3)
        elif(direction == "left"):
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                time.sleep(0.5)
                Movement.Left()
                direction = ""
                time.sleep(3)
                orientation -=1
        elif(direction == "backward"):
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                time.sleep(0.5)
                Movement.Turn180()
                direction = ""
                time.sleep(3)
                orientation +=2
        elif((Sensors[4] >650 or Sensors[0] >650)):
                Ab.stop()
                Ab.setPWMA(20)
                Ab.setPWMA(20)
                Ab.forward()
                time.sleep(0.04)
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                Ab.stop()
                position,Sensors = TR.readLine()
                if((Sensors[4] + Sensors[3]) > 900):
                    right = 0
                if((Sensors[0] + Sensors[1]) > 900):
                    left = 0
                Ab.setPWMA(20)
                Ab.setPWMB(20)
                Ab.forward()
                time.sleep(0.18)
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                position,Sensors = TR.readLine()
                if((Sensors[1] + Sensors[2] + Sensors[3]) > 1000):
                    forward = 0
                time.sleep(3)
        elif(Sensors[0] < 100 and Sensors[1] < 100 and Sensors[2] < 100 and Sensors[3] < 100 and Sensors[4] < 100):
                Ab.stop()
                Ab.setPWMA(0)
                Ab.setPWMB(0)
                time.sleep(3)
                Movement.DeadEndTurn()
                orientation+=2
                time.sleep(3)
                Movement.Forward()
                distance = 0
        else:
                newDistance = Movement.Forward()
                if(newDistance > 0):
                        distance = newDistance


corners =dijkstra.FindShortesPath()
corners.pop()
while True:
        Movement.Forward()
        Ab.stop()
        position,Sensors = TR.readLine()
        if(Sensors[0] <300 and Sensors[1] < 300 and Sensors[2] < 300 and Sensors[3] < 300 and Sensors[4] < 300 and
                Sensors[0] > 100 and Sensors[1] > 100 and Sensors[2] > 100 and Sensors[3] > 100 and Sensors[4] > 100):
                break
        Ab.setPWMA(20)
        Ab.setPWMB(20)
        Ab.forward()
        time.sleep(0.18)
        Ab.stop()
        Ab.setPWMA(0)
        Ab.setPWMB(0)
        corner = corners.pop()
        nextCorner = corners.__getitem__(-1)
        direction = corner.GetDirection(orientation, nextCorner)
        if(direction == "Right"):
                time.sleep(0.5)
                Movement.Right()
                time.sleep(2)
                direction = ""
                orientation +=1
        elif(direction == "Forward"):
                direction = ""
                time.sleep(2)
        elif(direction == "Left"):
                time.sleep(0.5)
                Movement.Left()
                time.sleep(2)
                orientation -=1
        if(orientation > 3):
                orientation -= 4
        elif(orientation < 0):
                orientation +=4