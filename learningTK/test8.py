import tkinter as tk

window = tk.Tk()
window.title("Image Rendering")

icon = tk.PhotoImage(file = "c:/Users/nsham/Downloads/happy-face.png")

label = tk.Label(window, image = icon)
label.pack()

window.mainloop()