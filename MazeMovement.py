import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from TRSensors import TRSensor

class MazeMovement(object):
        def __init__(self, Ab, TR, speed = 25):
                self.TR = TR
                self.Ab = Ab
                self.maximum = speed
                self.integral = 0
                self.last_proportional = 0
                self.Ab.setPWMA(speed)
                self.Ab.setPWMB(speed)

        
        def Forward(self):
                self.Ab.setPWMA(self.maximum)
                self.Ab.setPWMB(self.maximum)
                distance = 0
                while(True):
                        position,Sensors = self.TR.readLine()
                        if(Sensors[0] > 650 or Sensors[4] > 650 or 
                                (Sensors[0] < 300 and Sensors[1] < 300 and Sensors[2] < 300 and Sensors[3] < 300 and Sensors[4] < 300)):
                                self.Ab.stop()
                                self.Ab.setPWMA(0)
                                self.Ab.setPWMB(0)
                                return distance
                        self.Ab.forward()
                        distance +=1
                        proportional = position - 2000

                        derivative = proportional - self.last_proportional
                        self.integral += proportional

                        self.last_proportional = proportional

                        power_difference = proportional/30  + self.integral/10000 + derivative*2;

                        if (power_difference > self.maximum):
                                power_difference = self.maximum
                        if (power_difference < - self.maximum):
                                power_difference = - self.maximum
                        if (power_difference < 0):
                                self.Ab.setPWMA(self.maximum + power_difference)
                                self.Ab.setPWMB(self.maximum)
                        else:
                                self.Ab.setPWMA(self.maximum)
                                self.Ab.setPWMB(self.maximum - power_difference)


        def Right(self):
                self.Ab.setPWMA(20)
                self.Ab.setPWMB(20)
                for i in range(0, 1000):
                        position,Sensors = self.TR.readLine()
                        self.Ab.right()
                        if(i > 150 and Sensors[2] > 250):
                                self.Ab.stop()
                                self.Ab.setPWMA(0)
                                self.Ab.setPWMB(0)
                                break
        
        def Left(self):
                self.Ab.setPWMA(20)
                self.Ab.setPWMB(20)
                for i in range(0, 1000):
                        position,Sensors = self.TR.readLine()
                        self.Ab.left()
                        if(i > 150 and Sensors[2] > 250):
                                self.Ab.stop()
                                self.Ab.setPWMA(0)
                                self.Ab.setPWMB(0)
                                break

        def Turn180(self):
                self.Ab.setPWMA(20)
                self.Ab.setPWMB(20)
                for i in range(0, 1000):
                        position,Sensors = self.TR.readLine()
                        self.Ab.right()
                        if(i > 400 and Sensors[2] > 250):
                                self.Ab.stop()
                                self.Ab.setPWMA(0)
                                self.Ab.setPWMB(0)
                                break

        def DeadEndTurn(self):
                position,Sensors = self.TR.readLine()
                while(Sensors[2] < 250):
                        position,Sensors = self.TR.readLine()
                        self.Ab.setPWMA(20)
                        self.Ab.setPWMB(20)
                        self.Ab.right()
                self.Ab.stop()
                self.Ab.setPWMA(0)
                self.Ab.setPWMB(0)

        def Calibrate(self):
                for i in range(0,100):
                        if(i<25 or i>= 75):
                                self.Ab.right()
                                self.Ab.setPWMA(30)
                                self.Ab.setPWMB(30)
                        else:
                                self.Ab.left()
                                self.Ab.setPWMA(30)
                                self.Ab.setPWMB(30)
                        self.TR.calibrate()
                self.Ab.stop()