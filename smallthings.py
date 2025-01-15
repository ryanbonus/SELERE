import tkinter as tk

def update_tank(value):
    # Update the height of the tank based on the slider value
    tank_height = int(value)  # Slider value
    canvas.coords(tank, 10, 200 - tank_height, 60, 200)  # Set tank coordinates
    canvas.itemconfig(tank, fill="green")  # Set tank color to green

# Create the main window
root = tk.Tk()
root.title("Vertical Slider with Tank")

# Create a Canvas to draw the tank
canvas = tk.Canvas(root, width=100, height=250)
canvas.pack()

# Draw the outline of the tank
canvas.create_rectangle(10, 10, 60, 200, outline="black", width=2)

# Create a vertical slider
slider = tk.Scale(root, from_=0, to=100, orient="vertical", command=update_tank)
slider.set(0)  # Initial value
slider.pack(pady=20)

# Create the tank inside the canvas (initial height is 0)
tank = canvas.create_rectangle(10, 200, 60, 200, fill="green")

# Start the Tkinter main loop
root.mainloop()
