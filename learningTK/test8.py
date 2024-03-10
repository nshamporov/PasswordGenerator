import tkinter as tk

window = tk.Tk()
window.title("Image Rendering")

icon = tk.PhotoImage(file = "../media/icon.png")

label = tk.Label(window, image = icon)
label.pack()

window.mainloop()