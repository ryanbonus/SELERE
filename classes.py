import threading
import time

# Class for Knee Motor
class KneeMotor:
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
        print("Extending Knee: Range [{}-{}], Speed {}, Acceleration {}".format(
            rangeOfMotionBottom, rangeOfMotionTop, speed, acceleration))
        # Simulate extension time
        time.sleep(1)

    def retract(self, rangeOfMotionTop, rangeOfMotionBottom, speed, acceleration):
        self.rangeOfMotionTop = rangeOfMotionTop
        self.rangeOfMotionBottom = rangeOfMotionBottom
        self.speed = speed
        self.acceleration = acceleration
        print("Retracting Knee: Range [{}-{}], Speed {}, Acceleration {}".format(
            rangeOfMotionBottom, rangeOfMotionTop, speed, acceleration))
        # Simulate retraction time
        time.sleep(1)

    def assist(self, torque):
        self.torque = torque
        print("Assisting Knee with Torque:", torque)

    def resist(self, torque):
        self.torque = torque
        print("Resisting Knee with Torque:", torque)


# Class for Ankle Motor, inheriting from Knee Motor
class AnkleMotor(KneeMotor):
    def __init__(self):
        super().__init__()  # Inherit all attributes and methods


# Class for User Interface
class UserInterface:
    def __init__(self):
        self.modeButton = False
        self.button1 = False
        self.button2 = False
        self.dialState = 0

    def press_mode_button(self):
        self.modeButton = True

    def release_mode_button(self):
        self.modeButton = False

    def press_button1(self):
        self.button1 = True

    def release_button1(self):
        self.button1 = False

    def press_button2(self):
        self.button2 = True

    def release_button2(self):
        self.button2 = False

    def set_dial_state(self, state):
        self.dialState = state
        print("Dial State Set to:", state)


# Exoskeleton Class containing modes and motors
class Exoskeleton:
    def __init__(self):
        self.modes = ["Mode 1", "Mode 2", "Mode 3"]
        self.currentMode = self.modes[0]
        self.kneeMotor = KneeMotor()
        self.ankleMotor = AnkleMotor()
        self.userInterface = UserInterface()

    def nextMode(self):
        current_index = self.modes.index(self.currentMode)
        self.currentMode = self.modes[(current_index + 1) % len(self.modes)]
        print("Switched to", self.currentMode)

    def check_conditions(self):
        # Loop to constantly check and apply conditions
        while True:
            # Mode switching with mode button
            if self.userInterface.modeButton:
                self.nextMode()
                self.userInterface.release_mode_button()  # Reset button press

            # Mode-specific behaviors
            if self.currentMode == "Mode 1":
                # Extend and retract knee while button1 is pressed
                if self.userInterface.button1:
                    self.kneeMotor.extend(100, 0, self.userInterface.dialState, 5)
                    self.kneeMotor.retract(100, 0, self.userInterface.dialState, 5) #this needs to happen before the menu pops back up, not after. This is important so that only one command is being handled by the motor at once

                # Extend and retract ankle while button2 is pressed
                if self.userInterface.button2:
                    self.ankleMotor.extend(100, 0, self.userInterface.dialState, 5) #this needs to happen before the menu pops back up, not after. This is important so that only one command is being handled by the motor at once
                    self.ankleMotor.retract(100, 0, self.userInterface.dialState, 5)

            elif self.currentMode == "Mode 2":
                # Apply assistive torque if button1 or button2 is pressed
                if self.userInterface.button1:
                    self.kneeMotor.assist(self.userInterface.dialState)
                if self.userInterface.button2:
                    self.ankleMotor.assist(self.userInterface.dialState)

            elif self.currentMode == "Mode 3":
                # Apply resistive torque if button1 or button2 is pressed
                if self.userInterface.button1:
                    self.kneeMotor.resist(self.userInterface.dialState)
                if self.userInterface.button2:
                    self.ankleMotor.resist(self.userInterface.dialState)

            # Wait before rechecking to prevent excessive CPU usage
            time.sleep(0.1)


# Function to start the Exoskeleton and its loop in a separate thread
def start_exoskeleton():
    exo = Exoskeleton()
    # Starting the check_conditions function in a new thread
    condition_thread = threading.Thread(target=exo.check_conditions)
    condition_thread.daemon = True
    condition_thread.start()

    # Simulate user inputs in the command line
    while True:
        command = input("Enter command (mode, button1, button2, dial, quit): ").strip().lower() #'dial' needs to be switched to the identifier 'button3', and the logic needs to change to be similar to how the mode button works

        if command == "mode":
            exo.userInterface.press_mode_button()
        elif command == "button1":
            exo.userInterface.press_button1()
            time.sleep(0.2)
            exo.userInterface.release_button1()
        elif command == "button2":
            exo.userInterface.press_button2()
            time.sleep(0.2)
            exo.userInterface.release_button2()
        elif command.startswith("dial"):
            try:
                _, value = command.split()
                exo.userInterface.set_dial_state(int(value))
            except ValueError:
                print("Invalid dial input. Please enter 'dial' followed by a number.")
        elif command == "quit":
            print("Exiting...")
            break
        else:
            print("Invalid command.")

# Run the program
start_exoskeleton()
