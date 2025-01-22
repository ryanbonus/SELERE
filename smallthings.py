import tkinter as tk

def update_tank(value):
    # Map slider value (100 to 0) to tank height (0 to 190)
    tank_height = int(value)  # Slider value (from 100 to 0)
    fill_height = 200 - tank_height*2  # Adjust for the canvas' coordinate system
    canvas.coords(tank_fill, 10, fill_height, 200, 200)  # Adjust the tank's fill position

# Create the main window with a larger size
root = tk.Tk()
root.title("Slider and Tank")
root.geometry("500x400")  # Set a larger window size

# Create a frame to hold the tank and slider side by side
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Create the canvas for the tank on the left with a larger size
canvas = tk.Canvas(frame, width=200, height=200, bg="lightgray")
canvas.grid(row=0, column=0, padx=20)

# Draw the outline of the tank
canvas.create_rectangle(10, 10, 200, 200, outline="black", width=2)

# Create the tank's fill (initially empty)
tank_fill = canvas.create_rectangle(10, 200, 200, 200, outline="black", fill="blue")

# Create the slider on the right with the same height as the tank
slider = tk.Scale(frame, from_=100, to=0, orient="vertical", command=update_tank, length=200)
slider.set(0)  # Start at 0
slider.grid(row=0, column=1, padx=20)

# Start the Tkinter event loop
root.mainloop()
