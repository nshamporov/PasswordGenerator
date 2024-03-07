import tkinter as tk
import tkinter.messagebox

# creating a tk window
window = tk.Tk()
window.title("Alert Box")

# creating an alert box 
tk.messagebox.showinfo("Alert message", "This is an alert box!")

# create a question for the user and based upon the response [Yes or No Question] display a message.
response = tk.messagebox.askquestion("Question", "How are you?")

# 'if/else' block where if user clicks on 'Yes' then it returns 1 else it returns 0. For each response you will display a message with the help of 'Label' method
if response == 1:
    tk.Label(window, text = "Im good").pack()
else:
    tk.Label(window, text = "Im bad").pack()

window.mainloop()