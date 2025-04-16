import pyCandle
import sys
import time
import math

# Create CANdle object and ping FDCAN bus in search of drives.
# Any found drives will be printed out by the ping() method.

def setupCandle():
    candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True)
    motors = candle.ping()
    candle.addMd80(motors)

    for motor in motors:
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.positionWindow, 0.05)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.velocityWindow, 1.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.profileAcceleration, 10.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.profileDeceleration, 5.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.profileVelocity, 15.0)
        candle.writeMd80Register(motor, pyCandle.Md80Reg_E.quickStopDeceleration, 200.0)
        candle.controlMd80SetEncoderZero(motor)                    #  Reset encoder at current position
        candle.controlMd80Enable(motor, True)                      # Enable the drive
    
    candle.begin()
    return (candle, motors) 

def position(candle, motor, id, position):
    candle.controlMd80Mode(motor, pyCandle.POSITION_PROFILE)   # Set mode to position profile
    candle.md80s[id].setTargetPosition(position)

def velocity(candle, motor, velocity):
    candle.controlMd80Mode(motor, pyCandle.VELOCITY_PROFILE)
    candle.md80s[id].setTargetVelocity(velocity)

def torque(candle, motor, id, torque):
    candle.controlMd80Mode(motor, pyCandle.RAW_TORQUE)
    candle.md80s[id].setTargetTorque(0.2)

def stopCandle(candle):
    candle.end()
