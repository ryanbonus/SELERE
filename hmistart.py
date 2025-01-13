import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Touch Screen Interface")
root.geometry("1024x600")  # Resolution for a 7" screen with typical aspect ratio

# Function placeholders for button actions
def set_mode(mode):
    print(f"Mode set to: {mode}")

def switch_tab(tab):
    print(f"Switched to {tab} tab")

def control_joint(joint):
    print(f"Controlling {joint}")

# Create frames for different sections
slider_frame = tk.Frame(root)
slider_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.7)

mode_frame = tk.Frame(root)
mode_frame.place(relx=0.05, rely=0.15, relwidth=0.25, relheight=0.15)

tab_frame = tk.Frame(root)
tab_frame.place(relx=0.7, rely=0.05, relwidth=0.25, relheight=0.2)

joint_frame = tk.Frame(root)
joint_frame.place(relx=0.4, rely=0.3, relwidth=0.35, relheight=0.5)

# Tank-style sliders
slider_height = 250
slider_width = 50

def update_intensity(val):
    # Flip the direction for intensity slider (start from bottom)
    intensity_tank.coords(intensity_fill, 0, slider_height - (slider_height * (float(val) / 100)), slider_width, slider_height)

def update_height(val):
    # Flip the direction for height slider (start from bottom)
    height_tank.coords(height_fill, 0, slider_height - (slider_height * (float(val) / 100)), slider_width, slider_height)

# Intensity tank
intensity_label = tk.Label(slider_frame, text="Intensity")
intensity_label.grid(row=0, column=0, padx=5, pady=5)
intensity_tank = tk.Canvas(slider_frame, width=slider_width, height=slider_height, bg="lightgray")
intensity_fill = intensity_tank.create_rectangle(0, slider_height, slider_width, slider_height, fill="blue")
intensity_tank.grid(row=1, column=0, padx=5, pady=5)
intensity_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="vertical", command=update_intensity)
intensity_slider.set(0)  # Set initial value to 0, which is at the bottom
intensity_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ns")

# Height tank
height_label = tk.Label(slider_frame, text="Height")
height_label.grid(row=0, column=2, padx=5, pady=5)
height_tank = tk.Canvas(slider_frame, width=slider_width, height=slider_height, bg="lightgray")
height_fill = height_tank.create_rectangle(0, slider_height, slider_width, slider_height, fill="green")
height_tank.grid(row=1, column=2, padx=5, pady=5)
height_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="vertical", command=update_height)
height_slider.set(0)  # Set initial value to 0, which is at the bottom
height_slider.grid(row=1, column=3, padx=5, pady=5, sticky="ns")

# Configure equal column widths
for i in range(4):
    slider_frame.grid_columnconfigure(i, weight=1)

# Ensure proper row configuration
slider_frame.grid_rowconfigure(1, weight=1)

# Mode buttons
modes = ["Mode 1", "Mode 2", "Mode 3"]
for idx, mode in enumerate(modes):
    mode_button = tk.Button(mode_frame, text=mode, command=lambda m=mode: set_mode(m), height=1)
    mode_button.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")

# Configure equal column widths for mode buttons
for i in range(len(modes)):
    mode_frame.grid_columnconfigure(i, weight=1)

# Adjusted mode_frame placement
mode_frame.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.1)

# Tab buttons
tabs = ["User", "Edit", "Analytics", "DOC"]
for tab in tabs:
    tab_button = tk.Button(tab_frame, text=tab, command=lambda t=tab: switch_tab(t), height=2, width=8)
    tab_button.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# Joint control buttons
joints = ["Left Knee", "Left Ankle", "Right Knee", "Right Ankle"]
row, col = 0, 0
for joint in joints:
    joint_button = tk.Button(joint_frame, text=joint, command=lambda j=joint: control_joint(j), height=3, width=8)
    joint_button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    col += 1
    if col > 1:
        col = 0
        row += 1

for i in range(2):
    joint_frame.grid_rowconfigure(i, weight=1)
    joint_frame.grid_columnconfigure(i, weight=1)

# Start the main loop
root.mainloop()
