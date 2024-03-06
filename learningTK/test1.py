import tkinter as tk

window = tk.Tk()

# to rename the title of the window
window.title("Creating Button")

# pack is used to show the object in the window
# This is a label widget which is used to display text
label = tk.Label(window, text="Test 1 window (Learning tkinter widgets)").pack()

# here is a button used to peform functions
button = tk.Button(window, text="Click me!")
button.pack()

# The mainloop() method is called to start the event loop, which waits for user input and responds to events such as button clicks or key presses
window.mainloop()