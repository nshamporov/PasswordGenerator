import tkinter as tk

# creating tk window
window = tk.Tk()
window.title("Mouse Clicking Event")

# creating three different functions for three events 
def left_click(event):
    tk.Label(window, text = "Left Click").pack()

def middle_click(event):
    tk.Label(window, text = "Middle click").pack()

def right_click(event):
    tk.Label(window, text = "Right click").pack()

window.bind("<Button-1>", left_click)
window.bind("<Button-2>", middle_click)
window.bind("<Button-3>", right_click)

window.mainloop()