import tkinter as tk

# creating tk window
window = tk.Tk()
window.title("Pack Placement")

# first create a division with the help of Frame class and align them on TOP and BOTTOM with pack() method
top_Frame = tk.Frame(window).pack()
bottom_Frame = tk.Frame(window).pack(side = "bottom")

# once the frames are created then you are all set to add widgets in both frames
btn1 = tk.Button(top_Frame, text = "Button1", fg = "red").pack() # fg or foreground is for coloring the contents (buttons in this case)

btn2 = tk.Button(top_Frame, text = "Button2", fg = "green").pack()

btn3 = tk.Button(bottom_Frame, text = "Button3", fg = "purple").pack(side = "left") #'side' is used to left or right align the widgets

btn4 = tk.Button(bottom_Frame, text = "Button4", fg = "orange").pack(side = "right")

window.mainloop()