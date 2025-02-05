import tkinter as tk
from tkinter import ttk
from classes import Exoskeleton
from kneeMotor.motorCAN import start_can

# Initialize main window
root = tk.Tk()
root.title("Touch Screen Interface")
root.geometry("1024x600")
exo = Exoskeleton()

# Variables to track selected mode, joint, and tab
selected_mode = tk.StringVar(value="Mode 1")
selected_joint = tk.StringVar(value="Left Knee")
selected_tab = tk.StringVar(value="Edit")

# Function placeholders for button actions
def set_mode(mode):
    if exo.currentMode.number != mode:  # Only change if it's different
        selected_mode.set(mode)
        update_button_colors()
        if mode in exo.modes:
            print(f"Mode set to: {mode}") #Todo, fix mode validation with new objects
            exo.currentMode = exo.modes[mode-1] 
        else:
            print(f"Mode {mode} does not exist")

def switch_tab(tab):
    if selected_tab.get() != tab:  # Only change if it's different
        selected_tab.set(tab)
        update_button_colors()
        update_visibility()
        print(f"Switched to {tab} tab")


def control_joint(joint):
    if selected_joint.get() != joint:  # Only change if it's different
        selected_joint.set(joint)
        update_button_colors()
        print(f"Controlling {joint}")
        if joint in exo.joints:
            exo.currentJoint = joint
        else:
            print(f"Joint {joint} does not exist")

# Function for Start button
def start_button_pressed():
    print("Start button clicked")
    exo.currentState = exo.states[1]

def start_button_released():
    print("Start button released")
    exo.currentState = exo.states[0]

# Create frames for different sections
slider_frame = tk.Frame(root)
slider_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.7)

mode_frame = tk.Frame(root)
mode_frame.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.1)

# Status frame with labels side by side
status_frame = tk.Frame(root)
status_frame.place(relx=0.05, rely=0.2, relwidth=0.25, relheight=0.08)

# Adjusted width and font size for the status labels
mode_status_label = tk.Label(status_frame, textvariable=selected_mode, font=("Arial", 28), relief="solid", width=7)
mode_status_label.pack(side="left", padx=5, pady=5, expand=True, fill="both")

joint_status_label = tk.Label(status_frame, textvariable=selected_joint, font=("Arial", 28), relief="solid", width=14)
joint_status_label.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# Tab frame placement
tab_frame = tk.Frame(root)
tab_frame.place(relx=0.425, rely=0.05, relwidth=0.5, relheight=0.2)

joint_frame = tk.Frame(root)
joint_frame.place(relx=-.4, rely=0.3, relwidth=0.55, relheight=0.55)

# Tank-style sliders
slider_heights = (0, 650)  # Change these values to modify the min and max values of the height and intensity sliders
slider_widths = (0, 50)


def update_intensity(val):
    intensity_tank.coords(intensity_fill, slider_widths[0], slider_heights[1] - (slider_heights[1] * (float(val) / 100)), slider_widths[1], slider_heights[1])

def update_height(val):
    height_tank.coords(height_fill, slider_widths[0], slider_heights[1], slider_widths[1], slider_heights[1] - (slider_heights[1] * (float(val) / 100)))
    
# Intensity tank
intensity_label = tk.Label(slider_frame, text="Intensity")
intensity_label.grid(row=0, column=0, padx=5, pady=5)
intensity_tank = tk.Canvas(slider_frame, width=slider_widths[1], height=slider_heights[1], bg="lightgray")
intensity_fill = intensity_tank.create_rectangle(slider_widths[0], slider_heights[0], slider_widths[1], slider_heights[0], fill="blue")
intensity_tank.grid(row=1, column=0, padx=5, pady=5)
intensity_slider = ttk.Scale(slider_frame, from_=100, to=0, orient="vertical", command=update_intensity)
intensity_slider.set(0)
intensity_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ns")

# Height tank
height_label = tk.Label(slider_frame, text="Height")
height_label.grid(row=0, column=2, padx=5, pady=5)
height_tank = tk.Canvas(slider_frame, width=slider_widths[1], height=slider_heights[1], bg="lightgray")
height_fill = height_tank.create_rectangle(slider_widths[0], slider_heights[0], slider_widths[1], slider_heights[0], fill="green")
height_tank.grid(row=1, column=2, padx=5, pady=5)
height_slider = ttk.Scale(slider_frame, from_=100, to=0, orient="vertical", command=update_height)
height_slider.set(0)
height_slider.grid(row=1, column=3, padx=5, pady=5, sticky="ns")

for i in range(4):
    slider_frame.grid_columnconfigure(i, weight=1)
slider_frame.grid_rowconfigure(1, weight=1)

# Mode buttons
mode_buttons = []
modes = [exo.modeFA, exo.modePA, exo.modePR]
for idx, mode in enumerate(modes):
    mode_button = tk.Button(mode_frame, text=mode.name, command=lambda m=mode.number: set_mode(m), height=3, width=15, font=("Arial", 28), activebackground="green")
    mode_button.grid(row=0, column=idx, padx=5, pady=5, sticky="nsew")
    mode_buttons.append(mode_button)

for i in range(len(modes)):
    mode_frame.grid_columnconfigure(i, weight=1)
mode_frame.grid_rowconfigure(0, weight=1)

# Tab buttons
tab_buttons = []
tabs = ["User", "Edit", "Analytics", "DOC"]
for tab in tabs:
    tab_button = tk.Button(
        tab_frame, 
        text=tab, 
        command=lambda t=tab: switch_tab(t), 
        font=("Arial", 28),
        height=1, 
        width=10, 
        activebackground="green"
    )
    tab_button.pack(side="left", padx=5, pady=5, expand=True, fill="both")
    tab_buttons.append(tab_button)

# Joint control buttons (adjusted height/width for larger boxes)
joint_buttons = []
joints = ["Left Knee", "Left Ankle", "Right Knee", "Right Ankle"]
row, col = 0, 0
for joint in joints:
    joint_button = tk.Button(joint_frame, text=joint, command=lambda j=joint: control_joint(j), height=6, width=20, font=("Arial", 50), activebackground="green")
    joint_button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
    joint_buttons.append(joint_button)
    col += 1
    if col > 1:
        col = 0
        row += 1

# Configure the grid so that the buttons stretch to fill the space
for i in range(2):
    joint_frame.grid_rowconfigure(i, weight=1)
for i in range(2):
    joint_frame.grid_columnconfigure(i, weight=1)

# Function to update button colors based on selection
def update_button_colors():
    for button, mode in zip(mode_buttons, modes):
        button.config(bg="green" if mode == selected_mode.get() else root.cget("bg"))

    for button, joint in zip(joint_buttons, joints):
        button.config(bg="green" if joint == selected_joint.get() else root.cget("bg"))

    for button, tab in zip(tab_buttons, tabs):
        button.config(bg="green" if tab == selected_tab.get() else root.cget("bg"))
# Declare max_intensity_value globally
# Declare max_intensity_value globally
max_intensity_value = None

def update_max_intensity(change):
    global max_intensity_value  # Reference the global variable
    # Get the current value from the label, adjust by change, and update it
    current_value = int(max_intensity_value.cget("text"))  # Get current value from the label
    new_value = current_value + change
    # Ensure the value doesn't go below 0
    if new_value < 0:
        new_value = 0
    # Update the label text with the new value
    max_intensity_value.config(text=str(new_value))

def create_intensity_buttons():
    global max_intensity_value  # Make sure to reference the global variable
    
    # Create a frame to hold the buttons and box, shift everything to the left
    intensity_button_frame = tk.Frame(root)
    intensity_button_frame.place(relx=0.03, rely=0.45, anchor="w")  # Shift further left

    # Buttons for the left side (-1, -5, -15)
    button_subtract_1 = tk.Button(intensity_button_frame, text="-1", font=("Arial", 12), command=lambda: update_max_intensity(-1))
    button_subtract_1.grid(row=0, column=0, padx=10, pady=2, sticky="w")  # Reduced pady
    
    button_subtract_5 = tk.Button(intensity_button_frame, text="-5", font=("Arial", 12), command=lambda: update_max_intensity(-5))
    button_subtract_5.grid(row=1, column=0, padx=10, pady=2, sticky="w")  # Reduced pady
    
    button_subtract_15 = tk.Button(intensity_button_frame, text="-15", font=("Arial", 12), command=lambda: update_max_intensity(-15))
    button_subtract_15.grid(row=2, column=0, padx=10, pady=2, sticky="w")  # Reduced pady

    # Create the max intensity label above the value box
    max_intensity_label = tk.Label(intensity_button_frame, text="Maximum Intensity", font=("Arial", 14))
    max_intensity_label.grid(row=0, column=1, columnspan=3, padx=10, pady=5, sticky="nsew")

    # Create the value box to show the intensity number in the middle
    max_intensity_value = tk.Label(intensity_button_frame, text="100", font=("Arial", 14), relief="solid", width=10, height=2)
    max_intensity_value.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="nsew")

    # Buttons for the right side (+1, +5, +15)
    button_add_1 = tk.Button(intensity_button_frame, text="+1", font=("Arial", 12), command=lambda: update_max_intensity(1))
    button_add_1.grid(row=0, column=4, padx=10, pady=2, sticky="e")  # Reduced pady
    
    button_add_5 = tk.Button(intensity_button_frame, text="+5", font=("Arial", 12), command=lambda: update_max_intensity(5))
    button_add_5.grid(row=1, column=4, padx=10, pady=2, sticky="e")  # Reduced pady
    
    button_add_15 = tk.Button(intensity_button_frame, text="+15", font=("Arial", 12), command=lambda: update_max_intensity(15))
    button_add_15.grid(row=2, column=4, padx=10, pady=2, sticky="e")  # Reduced pady
    
    # Adjust column weights to create spacing
    intensity_button_frame.grid_columnconfigure(0, weight=1)
    intensity_button_frame.grid_columnconfigure(1, weight=2)
    intensity_button_frame.grid_columnconfigure(2, weight=2)
    intensity_button_frame.grid_columnconfigure(3, weight=1)
    intensity_button_frame.grid_columnconfigure(4, weight=1)

def update_visibility():
    global max_intensity_value  # Ensure we reference the global variable
    
    mode_frame.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.1)
    status_frame.place(relx=0.05, rely=0.2, relwidth=0.25, relheight=0.08)

    if selected_tab.get() == "Edit":
        slider_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.7)
        joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)
        root.update_idletasks()
        root.tk.call("raise", intensity_tank._w)
        root.tk.call("raise", height_tank._w)
        try:
            button_tank_frame.place_forget()
        except NameError:
            pass
    elif selected_tab.get() == "DOC":
        joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)
        slider_frame.place_forget()

        # Show maximum intensity box in DOC tab, move it to the bottom-left corner
       # max_intensity_label = tk.Label(root, text="Maximum Intensity", font=("Arial", 14))
       # max_intensity_label.place(relx=0.12, rely=0.4, anchor="w")
        
        max_intensity_value = tk.Label(root, text="100", font=("Arial", 14), relief="solid", width=10, height=2)
        max_intensity_value.place(relx=0.12, rely=0.45, anchor="w")
        
        # Create intensity buttons
        create_intensity_buttons()

        try:
            button_tank_frame.place_forget()
        except NameError:
            pass
    else:
        joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)
        slider_frame.place_forget()
        button_tank_frame = tk.Frame(root)
        button_tank_frame.place(x=50, y=350, width=700, height=560)
        start_button = tk.Button(button_tank_frame, text="Start", height=6, width=10, font=("Arial", 50))
        start_button.place(x=0, y=0, width=500, height=560)
        start_button.bind("<ButtonPress", start_button_pressed)
        start_button.bind("<ButtonRelease", start_button_released)        
        blank_tank = tk.Canvas(button_tank_frame, bg="lightgray")
        blank_tank.place(x=550, y=0, width=100, height=560)

# Set initial button colors and visibility
update_button_colors()
update_visibility()

# Start the main loop
root.mainloop()
