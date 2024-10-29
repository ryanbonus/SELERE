import tkinter as tk

class ModeSwitcher:
    def __init__(self, root):
        self.root = root
        self.modes = ["Mode 1", "Mode 2", "Mode 3"]
        self.current_mode = 0
        self.knee_counter = 0
        self.ankle_counter = 0
        self.knee_running = False  # Controls if the knee counter is incrementing
        self.ankle_running = False  # Controls if the ankle counter is incrementing
        self.knee_direction = 1  # 1 for up, -1 for down
        self.ankle_direction = 1

        # Label to display the current mode
        self.label = tk.Label(root, text=self.modes[self.current_mode], font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Button to switch modes
        self.mode_button = tk.Button(root, text="Switch Mode", command=self.switch_mode, font=("Helvetica", 16))
        self.mode_button.pack(pady=10)

        # Labels to display the counter values
        self.knee_label = tk.Label(root, text="Knee Joint: 0", font=("Helvetica", 16))
        self.knee_label.pack(pady=10)

        self.ankle_label = tk.Label(root, text="Ankle Joint: 0", font=("Helvetica", 16))
        self.ankle_label.pack(pady=10)

        # Buttons to start/stop each counter
        self.knee_button = tk.Button(root, text="Start/Stop Knee Counter", command=self.toggle_knee_counter, font=("Helvetica", 16))
        self.knee_button.pack(pady=10)

        self.ankle_button = tk.Button(root, text="Start/Stop Ankle Counter", command=self.toggle_ankle_counter, font=("Helvetica", 16))
        self.ankle_button.pack(pady=10)

        # Speed dial (Scale widget) for Mode 1
        self.speed_dial = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Speed (Inverse)")
        self.speed_dial.set(50)
        self.speed_dial.pack(pady=10)

        # Torque dial (Scale widget) for Mode 2
        self.torque_dial = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Torque (Inverse)")
        self.torque_dial.set(50)
        self.torque_dial.pack(pady=10)
        self.torque_dial.pack_forget()  # Hide initially

        # To keep updating the counters in the background when needed
        self.update_counters()

    def switch_mode(self):
        # Cycle through modes
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        # Update label to show the current mode
        self.label.config(text=self.modes[self.current_mode])

        # Reset counters if we switch modes
        self.knee_running = False
        self.ankle_running = False

        # Show speed dial in Mode 1, torque dial in Mode 2, and hide both in Mode 3
        if self.current_mode == 0:
            self.speed_dial.pack(pady=10)
            self.torque_dial.pack_forget()
        elif self.current_mode == 1:
            self.speed_dial.pack_forget()
            self.torque_dial.pack(pady=10)
        else:
            self.speed_dial.pack_forget()
            self.torque_dial.pack_forget()

    def toggle_knee_counter(self):
        # Only allow the knee counter to run in Mode 1 or Mode 2
        if self.current_mode in [0, 1]:
            self.knee_running = not self.knee_running

    def toggle_ankle_counter(self):
        # Only allow the ankle counter to run in Mode 1 or Mode 2
        if self.current_mode in [0, 1]:
            self.ankle_running = not self.ankle_running

    def update_counters(self):
        # Get the delay based on the active mode's control dial
        if self.current_mode == 0:  # Speed control in Mode 1
            delay = 101 - self.speed_dial.get()
        elif self.current_mode == 1:  # Torque control in Mode 2
            delay = 101 - self.torque_dial.get()
        else:
            delay = 100  # Default delay in Mode 3, counters won't run here

        # Update knee counter
        if self.knee_running and self.current_mode in [0, 1]:
            # Update counter based on direction
            self.knee_counter += self.knee_direction

            # Reverse direction at bounds (0 and 100)
            if self.knee_counter >= 100:
                self.knee_counter = 100
                self.knee_direction = -1
            elif self.knee_counter <= 0:
                self.knee_counter = 0
                self.knee_direction = 1

            # Update the knee label
            self.knee_label.config(text=f"Knee Joint: {self.knee_counter}")

        # Update ankle counter
        if self.ankle_running and self.current_mode in [0, 1]:
            # Update counter based on direction
            self.ankle_counter += self.ankle_direction

            # Reverse direction at bounds (0 and 100)
            if self.ankle_counter >= 100:
                self.ankle_counter = 100
                self.ankle_direction = -1
            elif self.ankle_counter <= 0:
                self.ankle_counter = 0
                self.ankle_direction = 1

            # Update the ankle label
            self.ankle_label.config(text=f"Ankle Joint: {self.ankle_counter}")

        # Schedule the next update
        self.root.after(delay, self.update_counters)

# Initialize the GUI application
root = tk.Tk()
root.title("Joint Counter Control")
app = ModeSwitcher(root)
root.mainloop()
