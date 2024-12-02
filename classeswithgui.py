import threading
import tkinter as tk

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

    def retract(self, rangeOfMotionTop, rangeOfMotionBottom, speed, acceleration):
        self.rangeOfMotionTop = rangeOfMotionTop
        self.rangeOfMotionBottom = rangeOfMotionBottom
        self.speed = speed
        self.acceleration = acceleration

    def assist(self, torque):
        self.torque = torque

    def resist(self, torque):
        self.torque = torque

# Ankle Motor class inheriting from Knee Motor
class AnkleMotor(KneeMotor):
    def __init__(self):
        super().__init__()

# User Interface class to manage user controls
class UserInterface:
    def __init__(self):
        self.modeButton = False
        self.button1 = False
        self.button2 = False
        self.dialState = 1

# Exoskeleton class to manage modes and motor states
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

# ModeSwitcher GUI class
class ModeSwitcher:
    def __init__(self, root):
        self.root = root
        self.exoskeleton = Exoskeleton()
        self.knee_counter = 0
        self.ankle_counter = 0
        self.knee_running = False
        self.ankle_running = False
        self.knee_direction = 1
        self.ankle_direction = 1

        # Mode display label
        self.label = tk.Label(root, text=self.exoskeleton.currentMode, font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Mode switch button
        self.mode_button = tk.Button(root, text="Switch Mode", command=self.switch_mode, font=("Helvetica", 16))
        self.mode_button.pack(pady=10)

        # Knee counter display label
        self.knee_label = tk.Label(root, text="Knee Joint: 0", font=("Helvetica", 16))
        self.knee_label.pack(pady=10)

        # Ankle counter display label
        self.ankle_label = tk.Label(root, text="Ankle Joint: 0", font=("Helvetica", 16))
        self.ankle_label.pack(pady=10)

        # Knee counter toggle button
        self.knee_button = tk.Button(root, text="Start/Stop Knee Counter", command=self.toggle_knee_counter, font=("Helvetica", 16))
        self.knee_button.pack(pady=10)

        # Ankle counter toggle button
        self.ankle_button = tk.Button(root, text="Start/Stop Ankle Counter", command=self.toggle_ankle_counter, font=("Helvetica", 16))
        self.ankle_button.pack(pady=10)

        # Dial controls with three levels only
        self.speed_dial = tk.Scale(root, from_=1, to=3, orient="horizontal", label="Speed Level")
        self.speed_dial.set(2)
        self.speed_dial.pack(pady=10)

        self.torque_dial = tk.Scale(root, from_=1, to=3, orient="horizontal", label="Torque Level")
        self.torque_dial.set(2)
        self.torque_dial.pack_forget()

        self.resistance_dial = tk.Scale(root, from_=1, to=3, orient="horizontal", label="Resistance Level")
        self.resistance_dial.set(1)
        self.resistance_dial.pack_forget()

        # Start update thread
        self.update_counters()

    def switch_mode(self):
        self.exoskeleton.nextMode()
        self.label.config(text=self.exoskeleton.currentMode)

        self.knee_running = False
        self.ankle_running = False

        if self.exoskeleton.currentMode == "Mode 1":
            self.speed_dial.pack(pady=10)
            self.torque_dial.pack_forget()
            self.resistance_dial.pack_forget()
        elif self.exoskeleton.currentMode == "Mode 2":
            self.speed_dial.pack_forget()
            self.torque_dial.pack(pady=10)
            self.resistance_dial.pack_forget()
        elif self.exoskeleton.currentMode == "Mode 3":
            self.speed_dial.pack_forget()
            self.torque_dial.pack_forget()
            self.resistance_dial.pack(pady=10)

    def toggle_knee_counter(self):
        self.knee_running = not self.knee_running

    def toggle_ankle_counter(self):
        self.ankle_running = not self.ankle_running

    def apply_resistance(self, counter_value, direction):
        resistance_level = self.resistance_dial.get()
        resistance_effect = resistance_level / 3
        return counter_value + direction * (1 - resistance_effect)

    def update_counters(self):
        if self.exoskeleton.currentMode == "Mode 1":
            delay = 101 - self.speed_dial.get() * 33
        elif self.exoskeleton.currentMode == "Mode 2":
            delay = 101 - self.torque_dial.get() * 33
        elif self.exoskeleton.currentMode == "Mode 3":
            delay = 50

        if self.knee_running:
            if self.exoskeleton.currentMode == "Mode 3":
                self.knee_counter = self.apply_resistance(self.knee_counter, self.knee_direction)
            else:
                self.knee_counter += self.knee_direction

            if self.knee_counter >= 100:
                self.knee_counter = 100
                self.knee_direction = -1
            elif self.knee_counter <= 0:
                self.knee_counter = 0
                self.knee_direction = 1

            self.knee_label.config(text=f"Knee Joint: {int(self.knee_counter)}")

        if self.ankle_running:
            if self.exoskeleton.currentMode == "Mode 3":
                self.ankle_counter = self.apply_resistance(self.ankle_counter, self.ankle_direction)
            else:
                self.ankle_counter += self.ankle_direction

            if self.ankle_counter >= 100:
                self.ankle_counter = 100
                self.ankle_direction = -1
            elif self.ankle_counter <= 0:
                self.ankle_counter = 0
                self.ankle_direction = 1

            self.ankle_label.config(text=f"Ankle Joint: {int(self.ankle_counter)}")

        self.root.after(int(delay), self.update_counters)

# Initialize GUI
root = tk.Tk()
root.title("Exoskeleton Control")
app = ModeSwitcher(root)
root.mainloop()
