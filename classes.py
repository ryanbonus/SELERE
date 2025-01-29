import threading
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


# Class for User Interface
class UserInterface:
    def __init__(self):
        self.startbutton = False
        self.mode = 1
        self.joint = "rightknee"
        self.intensity = 0
        self.height = 0



# Exoskeleton Class containing modes and motors
class Exoskeleton:
    def __init__(self, canbus):
        self.modes = ["Mode 1", "Mode 2", "Mode 3"]
        self.currentMode = self.modes[0]
        self.kneeMotor = KneeMotor(canbus)
        self.ankleMotor = AnkleMotor()
        self.userInterface = UserInterface()
    
    def __init__(self, canbus, userInterface):
        self.modes = ["Mode 1", "Mode 2", "Mode 3"]
        self.currentMode = self.modes[0]
        self.kneeMotor = KneeMotor(canbus)
        self.ankleMotor = AnkleMotor()
        self.userInterface = userInterface

    def nextMode(self):
        current_index = self.modes.index(self.currentMode)
        self.currentMode = self.modes[(current_index + 1) % len(self.modes)]
        print("Switched to", self.currentMode)

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
.78
 
# Function to start the Exoskeleton and its loop in a separate thread
def start_exoskeleton(canbus):
    exo = Exoskeleton(canbus)

    while True:
        command = input("Enter command (mode, button1, button2, button3, quit): ").strip().lower()

        if command == "mode":
            exo.userInterface.press_mode_button()
            exo.nextMode()
            exo.userInterface.release_mode_button()
        elif command == "button1":
            exo.userInterface.press_button1()
            exo.handle_knee_motor()  # Button1 controls Knee Motor
            exo.userInterface.release_button1()
        elif command == "button2": 
            exo.userInterface.press_button2()
            exo.handle_ankle_motor()  # Button2 controls Ankle Motor
            exo.userInterface.release_button2()
        elif command == "button3":
            exo.userInterface.press_button3()
            exo.userInterface.release_button3()
        elif command == "quit":
            print("Exiting...")
            break
        else:
            print("Invalid command.")

# Run the program
kneeMotor.motorCAN.start_can(start_exoskeleton)
