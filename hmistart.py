import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Touch Screen Interface")
root.geometry("1024x600")

# Variables to track selected mode and joint
selected_mode = tk.StringVar(value="Mode 1")
selected_joint = tk.StringVar(value="Left Knee")

# Function placeholders for button actions
def set_mode(mode):
    selected_mode.set(mode)
    print(f"Mode set to: {mode}")

def switch_tab(tab):
    print(f"Switched to {tab} tab")

def control_joint(joint):
    selected_joint.set(joint)
    print(f"Controlling {joint}")

# Create frames for different sections
slider_frame = tk.Frame(root)
slider_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.7)

mode_frame = tk.Frame(root)
mode_frame.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.1)

# Status frame with labels side by side
status_frame = tk.Frame(root)
status_frame.place(relx=0.05, rely=0.2, relwidth=0.25, relheight=0.08)  # Increased relheight

# Increased width and adjusted padding for better visibility
mode_status_label = tk.Label(status_frame, textvariable=selected_mode, font=("Arial", 16), relief="solid", width=12)
mode_status_label.pack(side="left", padx=5, pady=5, expand=True, fill="both")

joint_status_label = tk.Label(status_frame, textvariable=selected_joint, font=("Arial", 16), relief="solid", width=12)
joint_status_label.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# Tab frame placement
tab_frame = tk.Frame(root)
tab_frame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.1)

joint_frame = tk.Frame(root)
joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)

# Tank-style sliders
slider_height = 250
slider_width = 50

def update_intensity(val):
    intensity_tank.coords(intensity_fill, 0, slider_height - (slider_height * (float(val) / 100)), slider_width, slider_height)

def update_height(val):
    height_tank.coords(height_fill, 0, slider_height - (slider_height * (float(val) / 100)), slider_width, slider_height)

# Intensity tank
intensity_label = tk.Label(slider_frame, text="Intensity")
intensity_label.grid(row=0, column=0, padx=5, pady=5)
intensity_tank = tk.Canvas(slider_frame, width=slider_width, height=slider_height, bg="lightgray")
intensity_fill = intensity_tank.create_rectangle(0, slider_height, slider_width, slider_height, fill="blue")
intensity_tank.grid(row=1, column=0, padx=5, pady=5)
intensity_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="vertical", command=update_intensity)
intensity_slider.set(0)
intensity_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ns")

# Height tank
height_label = tk.Label(slider_frame, text="Height")
height_label.grid(row=0, column=2, padx=5, pady=5)
height_tank = tk.Canvas(slider_frame, width=slider_width, height=slider_height, bg="lightgray")
height_fill = height_tank.create_rectangle(0, slider_height, slider_width, slider_height, fill="green")
height_tank.grid(row=1, column=2, padx=5, pady=5)
height_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="vertical", command=update_height)
height_slider.set(0)
height_slider.grid(row=1, column=3, padx=5, pady=5, sticky="ns")

for i in range(4):
    slider_frame.grid_columnconfigure(i, weight=1)
slider_frame.grid_rowconfigure(1, weight=1)

# Mode buttons
modes = ["Mode 1", "Mode 2", "Mode 3"]
for idx, mode in enumerate(modes):
    mode_button = tk.Button(mode_frame, text=mode, command=lambda m=mode: set_mode(m), height=3, width=15)
    mode_button.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")

for i in range(len(modes)):
    mode_frame.grid_columnconfigure(i, weight=1)
mode_frame.grid_rowconfigure(0, weight=1)

# Tab buttons
tabs = ["User", "Edit", "Analytics", "DOC"]
for tab in tabs:
    tab_button = tk.Button(tab_frame, text=tab, command=lambda t=tab: switch_tab(t))
    tab_button.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# Joint control buttons
joints = ["Left Knee", "Left Ankle", "Right Knee", "Right Ankle"]
row, col = 0, 0
for joint in joints:
    joint_button = tk.Button(joint_frame, text=joint, command=lambda j=joint: control_joint(j), height=6, width=20)
    joint_button.grid(row=row, column=col, padx=40, pady=40, sticky="nsew")
    col += 1
    if col > 1:
        col = 0
        row += 1

for i in range(2):
    joint_frame.grid_rowconfigure(i, weight=1)
for i in range(2):
    joint_frame.grid_columnconfigure(i, weight=1)

# Start the main loop
root.mainloop()
