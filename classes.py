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
        self.modes = [1,2,3]
        self.currentMode = self.modes[0]
        self.kneeMotor = KneeMotor(canbus)
        self.ankleMotor = AnkleMotor()

    def handle_knee_motor(self):
        if self.currentMode == "Mode 1":
            self.kneeMotor.extend(100, 0, self.userInterface.button3_state*1000, 5000)
            self.kneeMotor.retract(100, 0, self.userInterface.button3_state*1000, 5000)
        # In Mode 2: Extend and retract the knee, with assisting torque
        elif self.currentMode == "Mode 2":
            self.kneeMotor.assist(self.userInterface.button3_state)  # Assist with torque
        # In Mode 3: Extend and retract the knee, with resisting torque
        elif self.currentMode == "Mode 3":
            self.kneeMotor.resist(self.userInterface.button3_state)  # Resist with torque
    
    def handle_ankle_motor(self):
        if self.currentMode == "Mode 1":
            self.ankleMotor.extend(100, 0, self.userInterface.button3_state, 5)
            self.ankleMotor.retract(100, 0, self.userInterface.button3_state, 5)
        # In Mode 2: Extend and retract the ankle, with assisting torque
        elif self.currentMode == "Mode 2":
            self.ankleMotor.assist(self.userInterface.button3_state)  # Assist with torque
        # In Mode 3: Extend and retract the ankle, with resisting torque
        elif self.currentMode == "Mode 3":
            self.ankleMotor.resist(self.userInterface.button3_state)  # Resist with torque
 

