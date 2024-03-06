import tkinter as tk

# creating tk window
window = tk.Tk()
window.title("Binding Functions")

# creatng a function called click_me()
def click_me():
    tk.Label(window, text = "Hello!").pack()

# creating a button
tk.Button(window, text = "Click me!", command = click_me).pack()

window.mainloop()