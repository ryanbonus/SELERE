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

        # Inverted Dial (Scale widget) to control speed of counter increment
        self.speed_dial = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Speed (Inverse)")
        self.speed_dial.set(50)  # Default speed (middle range)
        self.speed_dial.pack(pady=10)

        # To keep updating the counters in the background when needed
        self.update_counters()

    def switch_mode(self):
        # Cycle through modes
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        # Update label to show the current mode
        self.label.config(text=self.modes[self.current_mode])

        # Reset counters if we switch modes
        self.knee_running = False  # Stop knee counter if switching modes
        self.ankle_running = False  # Stop ankle counter if switching modes

    def toggle_knee_counter(self):
        # Only allow the knee counter to run in Mode 1
        if self.current_mode == 0:
            self.knee_running = not self.knee_running

    def toggle_ankle_counter(self):
        # Only allow the ankle counter to run in Mode 1
        if self.current_mode == 0:
            self.ankle_running = not self.ankle_running

    def update_counters(self):
        # Update knee counter
        if self.knee_running and self.current_mode == 0:
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
        if self.ankle_running and self.current_mode == 0:
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

        # Calculate the inverse speed based on dial position (lower dial value = faster speed)
        speed_delay = 101 - self.speed_dial.get()  # Inverts the scale: 1 is fastest, 100 is slowest
        self.root.after(speed_delay, self.update_counters)

# Initialize the GUI application
root = tk.Tk()
root.title("Joint Counter Control")
app = ModeSwitcher(root)
root.mainloop()
