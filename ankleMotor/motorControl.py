import pyCandle
import sys
import time
import math

candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True)
# Create CANdle object and ping FDCAN bus in search of drives.
# Any found drives will be printed out by the ping() method.

def setupCandle():
    
    motors = candle.ping()

    for motor in motors:
        candle.addMd80(motor)

    for motor in motors:
        candle.md80s[motors.index(motor)].setPositionControllerParams(0.05, 0.5, 0.0, 1.5) #Ki, Kp Kd, iWindup
        candle.md80s[motors.index(motor)].setVelocityControllerParams(0.05, 0.5, 0.0, 1.5) #Ki, Kp Kd, iWindup
        setVelocity(motor)
    return (candle, motors) 

def position(id, index, position):
    candle.end()
    candle.controlMd80Enable(id, False)
    candle.controlMd80Mode(id, pyCandle.POSITION_PID)   # Set mode to position profile
    candle.controlMd80Enable(id, True)                      # Enable the drive
    candle.begin()        
    candle.md80s[index].setTargetPosition(position)

    while not candle.md80s[index].isTargetPositionReached():
        time.sleep(0.1)
    
    stopCandle()

def setVelocity(id):
    candle.end()
    candle.controlMd80Enable(id, False)  
    candle.controlMd80Mode(id, pyCandle.VELOCITY_PID)
    candle.controlMd80Enable(id, True) 
    candle.begin() 

def setTorque(id):
    candle.end()
    candle.controlMd80Enable(id, False)
    candle.controlMd80Mode(id, pyCandle.RAW_TORQUE)
    candle.controlMd80Enable(id, True) 
    candle.begin() 

def velocity(id, index, velocity):

    candle.md80s[index].setTargetVelocity(velocity)

def torque(id, index, torque):    
    candle.md80s[index].setTargetTorque(torque)

def stopCandle():
    candle.end()



def main():
    candleObjects = setupCandle()
    while True:
        choice = input()
        if choice == "1":
            position(candleObjects[1][0], 0, math.pi/4)
            stopCandle(candleObjects[0])
            position(candleObjects[1][0], 0, 0)
            stopCandle(candleObjects[0])

        if choice == "2":
            velocity(candleObjects[1][0], 0, -0.5)
            time.sleep(2)
            stopCandle(candleObjects[0])
            velocity(candleObjects[1][0], 0, 0.5)
            time.sleep(2)
            stopCandle(candleObjects[0])
            velocity(candleObjects[1][0], 0, 0)
            stopCandle(candleObjects[0])

        if choice == "3":
            torque(candleObjects[1][0], 0, 1)
            time.sleep(10)
            stopCandle(candleObjects[0])
            torque(candleObjects[1][0], 0, 0)
            stopCandle(candleObjects[0])

if __name__ == "__main__":
    main()
