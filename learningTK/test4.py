import tkinter as tk

# creating the TK window
window = tk.Tk()
window.title("Login Page")

# creating two labels named username and password and two input boxes for them
tk.Label(window, text = "Usename").grid(row = 0) # username is placed on position 00 (row - 0 and column - 0)

# Entry class is used to display the input field for username label
tk.Entry(window).grid(row = 0, column = 1) # first input field is placed on position 01 (row - 0 and column - 1)

tk.Label(window, text = "Password").grid(row = 1) # password is placed on position 10 (row - 1 and column - 0)

tk.Entry(window).grid(row = 1, column = 1) #second input field is placed on position 11 (row - 1 and column - 1)

# creating check box for keep me loged in. We use grid(columnspan) to take width of 2 columns and place the check box in the middle
tk.Checkbutton(window, text = "Keep Me Logged In").grid(columnspan = 2)

window.mainloop()