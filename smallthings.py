import tkinter as tk

def update_tank(value):
    # Update the height of the tank based on the slider value
    tank_height = int(value)  # Slider value directly affects the tank height
    # Ensure the tank fills proportionally
    canvas.coords(tank, 10, 200 - tank_height, 60, 200)  # Set tank coordinates based on slider value
    canvas.itemconfig(tank, fill="green")  # Set tank color to green

# Create the main window
root = tk.Tk()
root.title("Vertical Slider with Tank")

# Create a Frame to arrange the slider and the canvas side by side
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a Canvas to draw the tank (height of 250)
canvas = tk.Canvas(frame, width=100, height=250)
canvas.grid(row=0, column=0)

# Draw the outline of the tank (adjust the coordinates to match the canvas height)
canvas.create_rectangle(10, 10, 60, 200, outline="black", width=2)

# Create a vertical slider that starts at the bottom with 0 at the bottom and goes up to 100
slider = tk.Scale(frame, from_=0, to=100, orient="vertical", command=update_tank, sliderlength=30, length=250)
slider.set(0)  # Initial value is 0, starting at the bottom
slider.grid(row=0, column=1, padx=10)

# Create the tank inside the canvas (initial height is 0, meaning empty)
tank = canvas.create_rectangle(10, 200, 60, 200, fill="green")

# Start the Tkinter main loop
root.mainloop()
