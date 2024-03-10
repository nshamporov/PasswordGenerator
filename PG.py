import tkinter as tk
import secrets
import string
import mysql.connector


# database connection
def database_config(username, password):
    connection = mysql.connector.connect(
        host = 'localhost',
        user = username,
        password = password
    )

    cursor = connection.cursor()

    # create an alert message with logs if table and database exist or not and that user logged in successfuly





class PasswordGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Password Generator")
        self.geometry("400x100")

        window = tk.Frame(self)
        window.pack(side = "top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (login, Main, PGpage, ViewP, EditP, DeleteP):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# class for login page
class login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        
        # title widgets
        title = tk.Label(self, text = "Please Log In.")
        title.grid(columnspan = 2)

        # username related widgets
        username_label = tk.Label(self, text = "Usename:")
        username_label.grid(row = 1, column = 0, sticky = 'es')

        self.username_field = tk.Entry(self)
        self.username_field.grid(row = 1, column = 1, sticky = 'ws')

        # password related widgets
        password_label = tk.Label(self, text = "Password:")
        password_label.grid(row = 2, column = 0, sticky = 'es')
        
        self.password_field = tk.Entry(self, show = "*")
        self.password_field.grid(row = 2, column = 1, sticky = 'ws')

        # submit button (to check if the information is right)
        submit_button = tk.Button(self, text = "Submit", command = self.send_username_password)  # change after database is done
        submit_button.grid(columnspan = 2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def send_username_password(self):
        username = self.username_field.get()
        password = self.password_field.get()
        database_config(username, password)
        self.controller.show_frame(Main)
        


        

# class for main page where you will choose what to do (after login page)
class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = tk.Label(self, text="Welcome to the Password Generator.")
        title.pack()
    
        PGbutton = tk.Button(self, text="Generate Password", command=lambda: controller.show_frame(PGpage))
        PGbutton.pack()




# class for password generating and adding account name (and sending to database)
class PGpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        # function that generates a password and gets account name 
        def generate_password(length=12, uppercase=True, digits=True, special_chars=True):
            
            # generating a password
            characters = string.ascii_lowercase

            if uppercase:
                characters += string.ascii_uppercase
            if digits:
                characters += string.digits
            if special_chars:
                characters += string.punctuation
            
            password = ''.join(secrets.choice(characters) for _ in range(length))
            return password
        
        password = generate_password()

        # function to re generate password
        def regenarate_password():
            password = generate_password()
            displaying_password.config(text = password)


        # password related widgets
        password_label = tk.Label(self, text = "Generated Password:  ")
        password_label.grid(row = 0, column = 0, sticky = 'es')

        displaying_password = tk.Label(self, text = password)
        displaying_password.grid(row = 0, column = 1)

        regenarate_button = tk.Button(self, text = "Re-Generate", command = regenarate_password)
        regenarate_button.grid(row = 0, column = 2, sticky = 'ws')


        # account name related widgets
        account_label = tk.Label(self, text = "Enter Account Name: ")
        account_label.grid(row = 1, column = 0, sticky = 'es')

        account_field = tk.Entry(self)
        account_field.grid(row = 1, column = 1, sticky = 's')


        # save and back buttons
        save_button = tk.Button(self, text = "Save")
        save_button.grid(row = 3, column = 1, sticky = 'ws')

        back_button = tk.Button(self, text = "Back", command = lambda:controller.show_frame(Main))
        back_button.grid(row = 3, column = 1, sticky = 'es')


        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)















class ViewP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class EditP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


class DeleteP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)




if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()

