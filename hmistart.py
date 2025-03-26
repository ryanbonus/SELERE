import tkinter as tk
from classes import Exoskeleton
from kneeMotor.motorCAN import start_can, tkinter_loop, comm_can_transmit_eid, write_log
from kneeMotor.motorControl import current, set_origin, speed
from PIL import Image, ImageTk

# Initialize main window
root = tk.Tk()
root.title("Touch Screen Interface")
root.geometry("1024x600")
root.configure(bg="lightgray")  
exo = Exoskeleton()

# Variables to track selected mode, joint, tab, and DOC button
selected_mode = tk.StringVar(value=exo.currentMode.name)
selected_joint = tk.StringVar(value=exo.currentJoint.name)
selected_tab = tk.StringVar(value="Edit")
selected_doc_button = tk.StringVar(value="Max Intensity")  # Add this line




# Add this function somewhere in your code (before the main loop)
def display_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((300, 200), Image.LANCZOS)  # Adjust size as needed
        photo = ImageTk.PhotoImage(img)
        return photo
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Add this variable near your other frame variables
image_frame = tk.Frame(root)
image_label = tk.Label(image_frame)
# Dictionary to store settings for each mode and joint
settings = {
    "Full": {
        "Left Knee": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Left Ankle": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Right Knee": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Right Ankle": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
    },
    "Partial": {
        "Left Knee": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Left Ankle": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Right Knee": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Right Ankle": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
    },
    "Resistance": {
        "Left Knee": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Left Ankle": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Right Knee": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
        "Right Ankle": {"max_intensity": 100, "min_intensity": 0, "max_height": 100, "min_height": 0, "current_intensity": 0, "current_height": 0},
    },
}

# Function to set the mode
def set_mode(mode):
    if exo.currentMode.number != mode.number:  # Only change if it's different
        selected_mode.set(mode.name)
        update_button_colors()
        if mode in exo.modes:
            print(f"Mode set to: {mode.name}") #Todo, fix mode validation with new objects
            exo.currentMode = exo.modes[mode.number-1] 
        else:
            print(f"Mode {mode.name} does not exist")
        
        update_sliders()  # Restore saved slider values
        update_button_labels()  # Update button labels

def switch_tab(tab):
    if selected_tab.get() != tab:  # Only change if it's different
        selected_tab.set(tab)
        update_button_colors()
        update_visibility()
        print(f"Switched to {tab} tab")

def control_joint(joint):
    if selected_joint.get() != joint.name:  # Only change if it's different
        selected_joint.set(joint.name)
        update_button_colors()  # Update button colors
        print(f"Controlling {joint.name}")
        if joint in exo.joints:
            exo.currentJoint = joint
        else:
            print(f"Joint {joint.name} does not exist")

        update_sliders()  # Restore saved slider values
        update_button_labels()  # Update labels when joint changes

# Function for Start button
def start_button_pressed(*args):
    print("Start button clicked")
    exo.currentState = exo.states[1]
    if exo.currentState == "started":
        run()

def run():
    if exo.currentState == "started":
        if exo.currentMode.name == "Full":
            position = exo.currentJoint.getPosition()
            print(position,'/',exo.currentJoint.desHeight)
            desSpd = exo.currentJoint.getDesSpeed()
            if position > exo.currentJoint.desHeight:
                exo.currentJoint.currentDirection = -1 * exo.currentJoint.initialDirection
            if position < exo.currentJoint.minHeight:
                exo.currentJoint.currentDirection = exo.currentJoint.initialDirection
            if exo.currentJoint.currentDirection == 1:
                comm_can_transmit_eid(*speed(exo.currentJoint.canbus, desSpd, controller_id=exo.currentJoint.id))
                #write_log(position)
            else:
                comm_can_transmit_eid(*speed(exo.currentJoint.canbus, -desSpd, controller_id=exo.currentJoint.id))
                #write_log(position)

        if exo.currentMode.name == "Partial" or "Resistance":
            desCurrent = exo.currentJoint.getDesCurrent()
            if exo.currentState == "started":
                if exo.currentMode.name == "Partial":
                    comm_can_transmit_eid(*current(exo.currentJoint.canbus, desCurrent, controller_id=exo.currentJoint.id))
                if exo.currentMode.name == "Resistance":
                    comm_can_transmit_eid(*current(exo.currentJoint.canbus, -desCurrent, controller_id=exo.currentJoint.id))
        root.after(1, run)
    else:
        comm_can_transmit_eid(*current(exo.currentJoint.canbus, 0, controller_id=exo.currentJoint.id))


    

def start_button_released(*args):
    print("Start button released")
    write_log(f"LeftKnee Position:{exo.leftKnee.getPosition()}")
    write_log(f"RightKnee Position:{exo.rightKnee.getPosition()}")
    exo.currentState = exo.states[0]

    

# Create frames for different sections
slider_frame = tk.Frame(root)
slider_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.7)

mode_frame = tk.Frame(root)
mode_frame.place(relx=0.01, rely=0.05, relwidth=0.05, relheight=0.1)

# Status frame with labels side by side
status_frame = tk.Frame(root)
status_frame.place(relx=0.05, rely=0.2, relwidth=0.25, relheight=0.08)

# Adjusted width and font size for the status labels
# Commented out the mode and joint status labels
# mode_status_label = tk.Label(status_frame, textvariable=selected_mode, font=("Arial", 28), relief="solid", width=7)
# mode_status_label.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# joint_status_label = tk.Label(status_frame, textvariable=selected_joint, font=("Arial", 28), relief="solid", width=14)
# joint_status_label.pack(side="left", padx=5, pady=5, expand=True, fill="both")

# Tab frame placement
tab_frame = tk.Frame(root)
tab_frame.place(relx=0.425, rely=0.05, relwidth=0.5, relheight=0.2)

joint_frame = tk.Frame(root)
joint_frame.place(relx=-.4, rely=0.3, relwidth=0.55, relheight=0.55)

# Tank-style sliders
slider_heights = (0, 650)  # Change these values to modify the min and max values of the height and intensity sliders
slider_widths = (0, 100)  # Increased width from 50 to 100

def update_sliders():
    mode = selected_mode.get()
    joint = selected_joint.get()

    # Restore saved values from settings
    intensity_value = settings[mode][joint]["current_intensity"]
    height_value = settings[mode][joint]["current_height"]

    # Update the sliders with the saved values
    intensity_slider.set(intensity_value)
    height_slider.set(height_value)




def update_intensity(val):
    mode = selected_mode.get()
    joint = selected_joint.get()
    
    # Store the value in settings
    settings[mode][joint]["current_intensity"] = int(float(val))
    
    intensity_tank.coords(intensity_fill, slider_widths[0], slider_heights[1] - (slider_heights[1] * (float(val) / 100)), slider_widths[1], slider_heights[1])
    exo.currentJoint.desSpd = (int(float(val)) / 100) * exo.currentJoint.maxSpd
    exo.currentJoint.desCurrent = (int(float(val)) / 100) * exo.currentJoint.maxCurrent


def update_height(val):
    mode = selected_mode.get()
    joint = selected_joint.get()

    # Store the value in settings
    settings[mode][joint]["current_height"] = int(float(val))

    height_tank.coords(height_fill, slider_widths[0], slider_heights[1], slider_widths[1], slider_heights[1] - (slider_heights[1] * (float(val) / 100)))
    exo.currentJoint.desHeight = ((int(float(val)) / 100) * exo.currentJoint.rangeOfMotion) + exo.currentJoint.minHeight

# Intensity tank
#intensity_label = tk.Label(text="Intensity", font=("Arial", 20))
#intensity_label.grid(row=0, column=0, padx=5, pady=5)
intensity_tank = tk.Canvas(slider_frame, width=slider_widths[1], height=slider_heights[1], bg="lightgray")
intensity_fill = intensity_tank.create_rectangle(slider_widths[0], slider_heights[0], slider_widths[1], slider_heights[0], fill="green")
intensity_tank.grid(row=1, column=0, padx=5, pady=5)

# Height tank
#height_label = tk.Label(text="Height", font=("Arial", 17))
#height_label.grid(row=0, column=2, padx=5, pady=5)
height_tank = tk.Canvas(slider_frame, width=slider_widths[1], height=slider_heights[1], bg="lightgray")
height_fill = height_tank.create_rectangle(slider_widths[0], slider_heights[0], slider_widths[1], slider_heights[0], fill="green")
height_tank.grid(row=1, column=2, padx=5, pady=5)

def create_text_box(parent, text, x, y, width, height, font_size):
    """
    Create a customizable text box.
    
    Args:
        parent: The parent widget (e.g., root or another frame).
        text: The default text to display in the box.
        x: The x-coordinate for placement.
        y: The y-coordinate for placement.
        width: The width of the text box.
        height: The height of the text box.
        font_size: The font size of the text.
    """
    text_box = tk.Entry(
        parent,
        font=("Arial", font_size),
        width=width,
        justify="center",
        bg="lightgray",
        fg="black",
        relief=tk.FLAT,  # Remove the border    
        bd=2
    )
    text_box.insert(0, text)  # Set default text
    text_box.place(x=x, y=y, width=width * 10, height=height * 20)  # Adjust width and height scaling as needed
    return text_box

# Create the Intensity text box
intensity_text_box = create_text_box(
    parent=root,  # Place in the main window
    text="Intensity",
    x=50,  # X-coordinate
    y=100,  # Y-coordinate
    width=23,  # Width of the text box
    height=3,  # Height of the text box
    font_size=35  # Font size
)

# Create the Height text box
height_text_box = create_text_box(
    parent=root,  # Place in the main window
    text="Height",
    x=250,  # X-coordinate
    y=150,  # Y-coordinate
    width=20,  # Width of the text box
    height=3,  # Height of the text box
    font_size=35  # Font size
)



# Intensity slider (using tk.Scale)
intensity_slider = tk.Scale(
    slider_frame, 
    from_=100, 
    to=0, 
    orient="vertical", 
    command=update_intensity, 
    length=400,  # Height of the slider
    width=80,    # Width of the slider (thickness)
    sliderlength=80,  # Length of the slider thumb
    troughcolor="lightgray",  # Color of the slider track
    bg="lightgray",  # Background color of the slider
    font=("Arial", 28)
)
intensity_slider.set(0)  # Set initial value to 0
intensity_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ns")

# Height slider (using tk.Scale)
height_slider = tk.Scale(
    slider_frame, 
    from_=100, 
    to=0, 
    orient="vertical", 
    command=update_height, 
    length=400,  # Height of the slider
    width=80,    # Width of the slider (thickness)
    sliderlength=80,  # Length of the slider thumb
    troughcolor="lightgray",  # Color of the slider track
    bg="lightgray",  # Background color of the slider
    font=("Arial", 28)
)
height_slider.set(0)  # Set initial value to 0
height_slider.grid(row=1, column=3, padx=5, pady=5, sticky="ns")

for i in range(4):
    slider_frame.grid_columnconfigure(i, weight=1)
slider_frame.grid_rowconfigure(1, weight=1)

# Mode buttons
mode_buttons = []
modes = [exo.modeFA, exo.modePA, exo.modePR]
for idx, mode in enumerate(modes):
    mode_button = tk.Button(
        mode_frame, 
        text=mode.name, 
        command=lambda m=mode: set_mode(m), 
        height=10,  # Further increased height
        width=1,  # Further increased width
        font=("Arial", 36),  # Further increased font size
        activebackground="green"
    )
    mode_button.pack(side="left", padx=5, pady=5, expand=True, fill="both")
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
joints = [exo.leftKnee, exo.leftAnkle, exo.rightKnee, exo.rightAnkle]
row, col = 0, 0
for joint in joints:
    joint_button = tk.Button(joint_frame, text=joint.name, command=lambda j=joint: control_joint(j), height=6, width=20, font=("Arial", 50), activebackground="green")
    joint_button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
    joint_buttons.append(joint_button)
    col += 1
    if col > 1:
        col = 0
        row += 1

# Create a frame for the DOC tab buttons
doc_button_frame = tk.Frame(root)

# Create StringVar variables to track values
max_intensity_var = tk.StringVar(value="Max Intensity\n100")
min_intensity_var = tk.StringVar(value="Min Intensity\n0")
max_height_var = tk.StringVar(value="Max Height\n100")
min_height_var = tk.StringVar(value="Min Height\n0")

# Create intensity and height buttons with labels + values (larger size)
max_intensity_button = tk.Button(doc_button_frame, textvariable=max_intensity_var, height=4, width=20, font=("Arial", 24), activebackground="green")
min_intensity_button = tk.Button(doc_button_frame, textvariable=min_intensity_var, height=4, width=20, font=("Arial", 24), activebackground="green")
max_height_button = tk.Button(doc_button_frame, textvariable=max_height_var, height=4, width=20, font=("Arial", 24), activebackground="green")
min_height_button = tk.Button(doc_button_frame, textvariable=min_height_var, height=4, width=20, font=("Arial", 24), activebackground="green")

# Place buttons in a 2x2 layout
max_intensity_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
min_intensity_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
max_height_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
min_height_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Configure the grid to stretch and fill the space
doc_button_frame.grid_rowconfigure(0, weight=1)
doc_button_frame.grid_rowconfigure(1, weight=1)
doc_button_frame.grid_columnconfigure(0, weight=1)
doc_button_frame.grid_columnconfigure(1, weight=1)

# Function to update button labels dynamically when values change
def update_button_labels():
    mode = selected_mode.get()
    joint = selected_joint.get()
    max_intensity_var.set(f"Max Intensity\n{settings[mode][joint]['max_intensity']}")
    min_intensity_var.set(f"Min Intensity\n{settings[mode][joint]['min_intensity']}")
    max_height_var.set(f"Max Height\n{settings[mode][joint]['max_height']}")
    min_height_var.set(f"Min Height\n{settings[mode][joint]['min_height']}")

# Function to handle button selection
def select_doc_button(label):
    selected_doc_button.set(label)
    update_doc_button_colors()

# Function to handle button click
def on_button_click(label):
    select_doc_button(label)

# Add button click bindings for each button
max_intensity_button.config(command=lambda: on_button_click("Max Intensity"))
min_intensity_button.config(command=lambda: on_button_click("Min Intensity"))
max_height_button.config(command=lambda: on_button_click("Max Height"))
min_height_button.config(command=lambda: on_button_click("Min Height"))

# Function to update button colors dynamically
def update_doc_button_colors():
    buttons = [
        (max_intensity_button, "Max Intensity"),
        (min_intensity_button, "Min Intensity"),
        (max_height_button, "Max Height"),
        (min_height_button, "Min Height")
    ]
    
    for button, label in buttons:
        button.config(bg="green" if selected_doc_button.get() == label else root.cget("bg"))

# Call this function whenever values change
update_button_labels()

# Configure the grid so that the buttons stretch to fill the space
for i in range(2):
    joint_frame.grid_rowconfigure(i, weight=1)
for i in range(2):
    joint_frame.grid_columnconfigure(i, weight=1)

# Function to update button colors based on selection
def update_button_colors():
    # Update mode buttons
    for button, mode in zip(mode_buttons, modes):
        button.config(bg="green" if mode.name == selected_mode.get() else root.cget("bg"))

    # Update joint buttons
    for button, joint in zip(joint_buttons, joints):
        button.config(bg="green" if joint.name == selected_joint.get() else root.cget("bg"))

    # Update tab buttons
    for button, tab in zip(tab_buttons, tabs):
        button.config(bg="green" if tab == selected_tab.get() else root.cget("bg"))
# Set initial button colors and visibility
update_button_colors()

def update_visibility():
    global button_tank_frame, start_button, blank_tank, image_frame, image_label
    
    # Preserve the relwidth of mode_frame (0.45)
    mode_frame.place(relx=0.01, rely=0.05, relwidth=0.40, relheight=0.15)
    status_frame.place(relx=0.05, rely=0.2, relwidth=0.25, relheight=0.08)

    if selected_tab.get() == "Edit":
        slider_frame.place(relx=0.05, rely=0.3, relwidth=0.25, relheight=0.7)
        joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)
        doc_button_frame.place_forget()
        new_button_frame.place_forget()
        intensity_text_box.place(x=100, y=230, width=230, height=60)
        height_text_box.place(x=350, y=230, width=200, height=60)
        image_frame.place_forget()
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
        doc_button_frame.place(relx=0.025, rely=0.225, relwidth=0.35, relheight=0.35)
        new_button_frame.place(relx=0.025, rely=0.625, relwidth=0.35, relheight=0.35)
        intensity_text_box.place_forget()
        height_text_box.place_forget()
        image_frame.place_forget()
        try:
            button_tank_frame.place_forget()
        except NameError:
            pass
        
    elif selected_tab.get() == "Analytics":
        joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)
        slider_frame.place_forget()
        doc_button_frame.place_forget()
        new_button_frame.place_forget()
        intensity_text_box.place_forget()
        height_text_box.place_forget()
        try:
            button_tank_frame.place_forget()
        except NameError:
            pass
        
        # Display image in bottom left
        photo = display_image("Assets/3stepCurrent.PNG")
        if photo:
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference

            image_frame.place(relx=0.05, rely=0.7, relwidth=0.2, relheight=0.25)
            image_label.pack(fill="both", expand=True)
    else:  # User tab
        joint_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.55)
        slider_frame.place_forget()
        doc_button_frame.place_forget()
        new_button_frame.place_forget()
        intensity_text_box.place_forget()
        height_text_box.place_forget()
        image_frame.place_forget()
        button_tank_frame = tk.Frame(root)
        button_tank_frame.place(x=50, y=350, width=700, height=560)
        start_button = tk.Button(button_tank_frame, text="Start", height=6, width=10, font=("Arial", 50))
        start_button.place(x=0, y=0, width=500, height=560)
        start_button.bind("<ButtonPress>", start_button_pressed)
        start_button.bind("<ButtonRelease>", start_button_released)  
        blank_tank = tk.Canvas(button_tank_frame, bg="lightgray")
        blank_tank.place(x=550, y=0, width=100, height=560)

# Create a frame for the new buttons
new_button_frame = tk.Frame(root)

# Function to update the selected value
def update_value(delta):
    mode = selected_mode.get()
    joint = selected_joint.get()
    selected = selected_doc_button.get()
    if selected == "Max Intensity":
        settings[mode][joint]["max_intensity"] += delta
    elif selected == "Min Intensity":
        settings[mode][joint]["min_intensity"] += delta
    elif selected == "Max Height":
        settings[mode][joint]["max_height"] += delta
    elif selected == "Min Height":
        settings[mode][joint]["min_height"] += delta
    update_button_labels()

# Create the new buttons
buttons = [
    ("+1", lambda: update_value(1)),
    ("+5", lambda: update_value(5)),
    ("+15", lambda: update_value(15)),
    ("-1", lambda: update_value(-1)),
    ("-5", lambda: update_value(-5)),
    ("-15", lambda: update_value(-15))
]

# Place the buttons in 2 rows and 3 columns
for idx, (text, command) in enumerate(buttons):
    button = tk.Button(new_button_frame, text=text, command=command, height=4, width=10, font=("Arial", 24), activebackground="green")  # Adjusted width to 10
    button.grid(row=idx // 3, column=idx % 3, padx=5, pady=5)

# Set initial button colors and visibility
update_button_colors()
update_visibility()

# Start the main loop
components = [exo.leftKnee, exo.rightKnee]
start_can(components, tkinter_loop, root.mainloop)                                                                                                                                                                             