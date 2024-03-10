import tkinter as tk

class PasswordGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Password Generator")
        self.geometry("500x400")

        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Main, PGpage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        h1 = tk.Label(self, text="Welcome to the Password Generator.")
        h1.pack()
        PGbutton = tk.Button(self, text="Generate Password", command=lambda: controller.show_frame(PGpage))
        PGbutton.pack()


class PGpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="smth").pack()
        tk.Button(self, text="smth", command=lambda: controller.show_frame(Main)).pack()




if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()



# def PGwindow():
#     mainPG = tk.Tk()
#     mainPG.title("Generator Page")
#     mainPG.geometry("300x200")

    

#     # function that generates a password and gets account name 
#     def generate_password(length=12, uppercase=True, digits=True, special_chars=True):
        
#         # generating a password
#         characters = string.ascii_lowercase

#         if uppercase:
#             characters += string.ascii_uppercase
#         if digits:
#             characters += string.digits
#         if special_chars:
#             characters += string.punctuation
        
#         password = ''.join(secrets.choice(characters) for _ in range(length))
        

#         # creating a window
#         generator_window = tk.Tk()
#         generator_window.title("Add Account")
#         generator_window.geometry("300x200")
        
#         tk.Label(generator_window, text = "Generated Password: " + password).pack()
#         tk.Label(generator_window, text = "Enter Account Name: ").pack()
#         tk.Entry(generator_window).pack()

#         tk.Button(generator_window, text = "Submit").pack()
#         generator_window.mainloop()





#     tk.Label(mainPG, text = "Would you like to generate a password?").pack()
#     tk.Button(mainPG, text = "Generate a Password", command = generate_password).pack()
#     mainPG.mainloop()

# if __name__ == "__main__":
#     PGwindow()





# def acc_name():
#     window = tk.Tk()
#     window.title("Add Account")
#     window.geometry("300x200")

#     tk.Label(window, text = "Account Name: ").grid(row = 0)
#     tk.Entry(window).grid(row = 0, column = 1)
#     window.mainloop()

#     tk.Button(window, text = "Submit")




# import secrets
# import string
# import importlib

# def generate_password(length=12, uppercase=True, digits=True, special_chars=True):
#     characters = string.ascii_lowercase

#     if uppercase:
#         characters += string.ascii_uppercase
#     if digits:
#         characters += string.digits
#     if special_chars:
#         characters += string.punctuation

#     password = ''.join(secrets.choice(characters) for _ in range(length))
#     return password

# def acc_name():
#     account = input("\nEnter the name of Website/App where you gonna use this password: ")
#     return account

# def generate():
#     title = "Password Generator"
#     print(f"\n{'=' * 10} {title} {'=' * 10}\n")

#     generated_password = generate_password(length=12, uppercase=True, digits=True, special_chars=True)

#     start = input("Press Enter to Generate Password\n")

#     if start == "":
#         print("Generated Password: ", generated_password)
#     else:
#         print("Generated Password: ", generated_password)

#     print("\n<-! Would you like to save it or generate a new one? !->")

#     while True:
#         retry_save = input("\n===> Enter (1) to save or (2) to re-generate: ")

#         if retry_save == "1":
#             database = importlib.import_module("database")
#             database.inserting()
#             break
#         elif retry_save == "2":
#             generated_password = generate_password()
#             print("\nNew Generated Password: ", generated_password)
#         else:
#             print("\n/ / / Wrong input. Try again. / / /")

# if __name__ == "__main__":
#     generate()