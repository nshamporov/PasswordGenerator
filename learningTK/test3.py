import tkinter as tk
from tkinter import *

window = tk.Tk()
window.title("Creating Checkboxes")

# IntVar() is used to store weather the box is checked or not
CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()

# creating the checkboxes with the labels next to it
tk.Checkbutton(window, text = "Python", variable = CheckVar1, onvalue = 1, offvalue = 0).grid(row = 0, sticky = W)
tk.Checkbutton(window, text = "Java", variable = CheckVar2, onvalue = 1, offvalue = 0).grid(row = 1, sticky = W)
tk.Checkbutton(window, text = "JavaScript", variable = CheckVar3, onvalue = 1, offvalue = 0).grid(row = 2, sticky = W)

window.mainloop()