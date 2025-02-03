import time
import kneeMotor.motorCAN
import kneeMotor.motorControl

# Class for Knee Motor
class KneeMotor:
    def __init__(self, canbus):
        self.position = 0
        self.speed = 0
        self.acceleration = 0
        self.torque = 0
        self.rangeOfMotionTop = 45
        self.rangeOfMotionBottom = 0
        self.canbus = canbus

    def __init__(self):
        self.position = 0
        self.speed = 0
        self.acceleration = 0
        self.torque = 0
        self.rangeOfMotionTop = 45
        self.rangeOfMotionBottom = 0
        self.canbus = 0

    def extend(self, rangeOfMotionTop, desiredPosition, desiredSpeed, desiredAcceleration):
        #self.rangeOfMotionTop = rangeOfMotionTop
        #self.rangeOfMotionBottom = rangeOfMotionBottom
        self.speed = desiredSpeed
        self.acceleration = desiredAcceleration
        print("Extending Knee: Range [{}-{}], desiredSpeed {}, desiredAcceleration {}".format(
            desiredPosition, rangeOfMotionTop, desiredSpeed, desiredAcceleration))
        kneeMotor.motorControl.position_speed_acceleration(self.canbus, self.rangeOfMotionTop-desiredPosition, desiredSpeed, desiredAcceleration)
        self.position = desiredPosition
        time.sleep(1)

    def retract(self, desiredPosition, rangeOfMotionBottom, desiredSpeed, desiredAcceleration):
        #self.rangeOfMotionTop = rangeOfMotionTop
        #self.rangeOfMotionBottom = rangeOfMotionBottom
        self.speed = desiredSpeed
        self.acceleration = desiredAcceleration
        kneeMotor.motorCAN.write_log("Retracting Knee: Range [{}-{}], desiredSpeed {}, desiredAcceleration {}".format(
             desiredPosition, rangeOfMotionBottom, desiredSpeed, desiredAcceleration), log_dir="logs")
        
        kneeMotor.motorControl.position_speed_acceleration(self.canbus, rangeOfMotionBottom-desiredPosition, desiredSpeed, desiredAcceleration)
        self.position=desiredPosition
        time.sleep(1)

    def assist(self, torque):
        self.torque = torque
        kneeMotor.motorControl.current(self.canbus, torque)
        kneeMotor.motorCAN.write_log("Assisting Knee with Torque:" + torque, log_dir="logs")
     
    def resist(self, torque):
        self.torque = torque
        kneeMotor.motorControl.current(self.canbus, torque)
        kneeMotor.motorCAN.write_log("Resisting Knee with Torque:", torque)



# Class for Ankle Motor
class AnkleMotor:
    def __init__(self):
        self.position = 0
        self.speed = 0
        self.acceleration = 0
        self.torque = 0
        self.rangeOfMotionTop = 100
        self.rangeOfMotionBottom = 0

    def extend(self, rangeOfMotionTop, rangeOfMotionBottom, speed, acceleration):
        self.rangeOfMotionTop = rangeOfMotionTop
        self.rangeOfMotionBottom = rangeOfMotionBottom
        self.speed = speed
        self.acceleration = acceleration
        print("Extending Ankle: Range [{}-{}], Speed {}, Acceleration {}".format(
            rangeOfMotionBottom, rangeOfMotionTop, speed, acceleration))
        time.sleep(1)

    def retract(self, rangeOfMotionTop, rangeOfMotionBottom, speed, acceleration):
        self.rangeOfMotionTop = rangeOfMotionTop
        self.rangeOfMotionBottom = rangeOfMotionBottom
        self.speed = speed
        self.acceleration = acceleration
        print("Retracting Ankle: Range [{}-{}], Speed {}, Acceleration {}".format(
            rangeOfMotionBottom, rangeOfMotionTop, speed, acceleration))
        time.sleep(1)

    def assist(self, torque):
        self.torque = torque
        print("Assisting Ankle with Torque:", torque)

    def resist(self, torque):
        self.torque = torque
        print("Resisting Ankle with Torque:", torque)     
        

# Exoskeleton Class containing modes and motors
class Exoskeleton:
    def __init__(self, canbus):
        self.modeFA = Mode("Full Assistance", 1)
        self.modePA = Mode("Partial Assistance", 2)
        self.modePR = Mode("Partial Resistance", 3)
        self.modes = (self.modeFA, self.modePA, self.modePR)
        self.currentMode = self.modes[0]
        self.canbus = canbus
        self.leftKnee = KneeMotor(self.Bus)
        self.leftAnkle = AnkleMotor(self.Bus)
        self.joints = (self.leftKnee, self.leftAnkle)
        self.currentJoint = self.joints[0]
        self.states = ("stoppped", "started")
        self.currentState = self.states[0]

    def __init__(self):
        self.modeFA = Mode(name = "Full Assistance", number = 1)
        self.modePA = Mode(name = "Partial Assistance", number = 2)
        self.modePR = Mode(name = "Partial Resistance", number = 3)
        self.modes = (self.modeFA, self.modePA, self.modePR)
        self.currentMode = self.modes[0]
        self.canbus = 0
        self.leftKnee = KneeMotor()
        self.leftAnkle = AnkleMotor()
        self.joints = (self.leftKnee, self.leftAnkle)
        self.currentJoint = self.joints[0]
        self.states = ("stoppped", "started")
        self.currentState = self.states[0]



class Mode:
    def __init__(name, number, self):
        self.name = name
        self.number = number
        self.height = (0,1) #format (minHeight, maxHeight)

 

