import tkinter as tk

def toggle_color():
    current_color = button.cget("bg")  # Get the current background color of the button
    new_color = "green" if current_color == "red" else "red"
    button.config(bg=new_color)

# Create the main window
root = tk.Tk()
root.title("Color Toggle Button")

# Create a button with initial color red
button = tk.Button(root, text="Click Me", bg="red", command=toggle_color)
button.pack(pady=20, padx=20)

# Start the Tkinter event loop
root.mainloop()
