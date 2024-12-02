import time

class ModeSwitcher:
    def __init__(self):
        self.modes = ["Mode 1", "Mode 2", "Mode 3"]
        self.current_mode = 0
        self.knee_counter = 0
        self.ankle_counter = 0
        self.knee_running = False
        self.ankle_running = False
        self.knee_direction = 1
        self.ankle_direction = 1
        self.speed = 50  # Default speed for Mode 1
        self.torque = 50  # Default torque for Mode 2
        self.resistance = 0  # Default resistance for Mode 3

    def switch_mode(self):
        # Cycle through modes
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        print(f"\nSwitched to {self.modes[self.current_mode]}")

    def toggle_knee_counter(self):
        if self.current_mode in [0, 1, 2]:
            self.knee_running = not self.knee_running
            state = "started" if self.knee_running else "stopped"
            print(f"Knee counter {state}.")

    def toggle_ankle_counter(self):
        if self.current_mode in [0, 1, 2]:
            self.ankle_running = not self.ankle_running
            state = "started" if self.ankle_running else "stopped"
            print(f"Ankle counter {state}.")

    def apply_resistance(self, counter_value, direction):
        resistance_effect = self.resistance / 100  # Convert to a fraction between 0 and 1
        return counter_value + direction * (1 - resistance_effect)

    def update_counters(self):
        # Get the delay based on the active mode's control dial
        if self.current_mode == 0:  # Speed control in Mode 1
            delay = 101 - self.speed
        elif self.current_mode == 1:  # Torque control in Mode 2
            delay = 101 - self.torque
        else:  # Resistance control in Mode 3
            delay = 50  # Fixed delay

        # Update knee counter
        if self.knee_running and self.current_mode in [0, 1, 2]:
            if self.current_mode == 2:
                self.knee_counter = self.apply_resistance(self.knee_counter, self.knee_direction)
            else:
                self.knee_counter += self.knee_direction

            # Reverse direction at bounds (0 and 100)
            if self.knee_counter >= 100:
                self.knee_counter = 100
                self.knee_direction = -1
            elif self.knee_counter <= 0:
                self.knee_counter = 0
                self.knee_direction = 1

            print(f"Knee Joint: {int(self.knee_counter)}")

        # Update ankle counter
        if self.ankle_running and self.current_mode in [0, 1, 2]:
            if self.current_mode == 2:
                self.ankle_counter = self.apply_resistance(self.ankle_counter, self.ankle_direction)
            else:
                self.ankle_counter += self.ankle_direction

            # Reverse direction at bounds (0 and 100)
            if self.ankle_counter >= 100:
                self.ankle_counter = 100
                self.ankle_direction = -1
            elif self.ankle_counter <= 0:
                self.ankle_counter = 0
                self.ankle_direction = 1

            print(f"Ankle Joint: {int(self.ankle_counter)}")

        # Delay to simulate real-time updates
        time.sleep(delay / 1000)  # Convert milliseconds to seconds

    def run(self):
        while True:
            # Display current mode
            self.update_counters()

            # User input
            command = input("\nEnter command (switch, toggle_knee, toggle_ankle, set_speed, set_torque, set_resistance, quit): ").strip().lower()
            
            if command == "switch":
                self.switch_mode()
            elif command == "toggle_knee":
                self.toggle_knee_counter()
            elif command == "toggle_ankle":
                self.toggle_ankle_counter()
            elif command == "set_speed":
                self.speed = int(input("Enter speed (1-100): "))
                print(f"Speed set to {self.speed}.")
            elif command == "set_torque":
                self.torque = int(input("Enter torque (1-100): "))
                print(f"Torque set to {self.torque}.")
            elif command == "set_resistance":
                self.resistance = int(input("Enter resistance (0-100): "))
                print(f"Resistance set to {self.resistance}.")
            elif command == "quit":
                print("Exiting...")
                break
            else:
                print("Invalid command. Please try again.")

# Initialize and run the application
if __name__ == "__main__":
    app = ModeSwitcher()
    app.run()
