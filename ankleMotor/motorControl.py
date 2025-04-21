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
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.positionWindow, 0.05)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.velocityWindow, 1.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.profileAcceleration, 10.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.profileDeceleration, 5.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.profileVelocity, 15.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.quickStopDeceleration, 200.0)
        candle.controlMd80SetEncoderZero(motor)                    #  Reset encoder at current position
    return (candle, motors) 

def position(motor, id, position):
    candle.controlMd80Enable(motor, False)
    candle.controlMd80Mode(motor, pyCandle.POSITION_PROFILE)   # Set mode to position profile
    candle.controlMd80Enable(motor, True)                      # Enable the drive
    candle.begin()        
    candle.md80s[id].setTargetPosition(position)

    while not candle.md80s[0].isTargetPositionReached():
        time.sleep(1)

def velocity(motor, id, velocity):
    candle.controlMd80Enable(motor, False)
    candle.controlMd80Mode(motor, pyCandle.VELOCITY_PROFILE)
    candle.controlMd80Enable(motor, True) 
    candle.begin() 
    candle.md80s[id].setTargetVelocity(velocity)

def torque(motor, id, torque):
    candle.controlMd80Enable(motor, False)
    candle.controlMd80Mode(motor, pyCandle.RAW_TORQUE)
    candle.controlMd80Enable(motor, True) 
    candle.begin()     
    candle.md80s[id].setTargetTorque(torque)

def stopCandle(candle):
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
