import tkinter as tk

class ModeSwitcher:
    def __init__(self, root):
        self.root = root
        self.modes = ["Mode 1", "Mode 2", "Mode 3"]
        self.current_mode = 0

        # Label to display the current mode
        self.label = tk.Label(root, text=self.modes[self.current_mode], font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Button to switch modes
        self.button = tk.Button(root, text="Switch Mode", command=self.switch_mode, font=("Helvetica", 16))
        self.button.pack(pady=20)

    def switch_mode(self):
        # Cycle through modes
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        # Update label to show the current mode
        self.label.config(text=self.modes[self.current_mode])

# Initialize the GUI application
root = tk.Tk()
root.title("Mode Switcher")
app = ModeSwitcher(root)
root.mainloop()
