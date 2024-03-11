import tkinter as tk
import secrets
import string
import mysql.connector
import tkinter.messagebox


# database connection
def database_config(username, password):
    try:
        global connection
        connection = mysql.connector.connect(
            host = 'localhost',
            user = username,
            password = password
        )
        global cursor
        cursor = connection.cursor()

        # creating database with table 
        cursor.execute("create database if not exists Passwords")
        cursor.execute("use Passwords")
        cursor.execute("create table if not exists GeneratedPasswords(id int auto_increment primary key, acc_name varchar(255), password varchar(12))")
        
        # creating status message for database
        cursor.execute("show databases like 'Passwords'")
        database_exist = cursor.fetchone()

        if database_exist:
            database_status = "--Database: / / / GOOD / / /" 
        else:
            database_status = "--Database: / / / BAD / / /"

        # creating status message for table
        cursor.execute("show tables like 'GeneratedPasswords'")
        table_exist = cursor.fetchone()

        if table_exist:
            table_status = "--Table: / / / GOOD / / /" 
        else:
            table_status = "--Table: / / / BAD / / /"

        # Status message boxs
        tk.messagebox.showinfo("Login Status.", f"You have successfully logged in!\n\n\t<-Logs->\n{database_status}\n{table_status}")
        return True

    except mysql.connector.Error as err:
        # wrong password alert box
        tk.messagebox.showinfo("Login Status.", "Wrong Password! Please try again.")
        return False
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


# saving passwords to the database
def inserting_password(account_name, generated_password):
    try:
        cursor.execute("insert into GeneratedPasswords (acc_name, password) values (%s, %s)", (account_name, generated_password))
        connection.commit()

        tk.messagebox.showinfo("Password Saved Status", "Congradulations, Your password has been saved successfully!")
        return True
    
    except mysql.connector.Error as err:
        tk.messagebox.showerror("Error", f"Error: {err}")
        return False
    
    finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


# class that creates the base of the app
class PasswordGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating main window
        self.title("Password Generator")
        self.geometry("400x100")

        window = tk.Frame(self)
        window.pack(side = "top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # displaying frames
        self.frames = {}
        for F in (login, Main, PGpage, ViewP, EditP, DeleteP):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # first frame to display
        self.show_frame(login)

    # function to display frames
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

    # function that sends username and password to database_config()
    def send_username_password(self):
        username = self.username_field.get()
        password = self.password_field.get()
        success = database_config(username, password)
        if success:
            self.controller.show_frame(Main)
        

# class for main page where you will choose what to do (after login page)
class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = tk.Label(self, text="Welcome to the Password Generator.")
        title.pack()
    
        PasswordGeneratorPage = tk.Button(self, text="Generate Password", command=lambda: controller.show_frame(PGpage))
        PasswordGeneratorPage.pack()


# class for password generating and adding account name (and sending to database)
class PGpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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
        
        self.password = generate_password()

        # function to re generate password
        def regenarate_password():
            self.password = generate_password()
            displaying_password.config(text = self.password)

        # password related widgets
        password_label = tk.Label(self, text = "Generated Password:  ")
        password_label.grid(row = 0, column = 0, sticky = 'es')

        displaying_password = tk.Label(self, text = self.password)
        displaying_password.grid(row = 0, column = 1)

        regenarate_button = tk.Button(self, text = "Re-Generate", command = regenarate_password)
        regenarate_button.grid(row = 0, column = 2, sticky = 'ws')


        # account name related widgets
        account_label = tk.Label(self, text = "Enter Account Name: ")
        account_label.grid(row = 1, column = 0, sticky = 'es')

        self.account_field = tk.Entry(self)
        self.account_field.grid(row = 1, column = 1, sticky = 's')


        # save and back buttons
        save_button = tk.Button(self, text = "Save", command = self.send_accName_GenPassword)
        save_button.grid(row = 3, column = 1, sticky = 'ws')

        back_button = tk.Button(self, text = "Back", command = lambda:controller.show_frame(Main))
        back_button.grid(row = 3, column = 1, sticky = 'es')


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    # function that sends acc_name and generated_password to inserting_password() 
    def send_accName_GenPassword(self):
        account_name = self.account_field.get()
        generated_password = self.password

        if not account_name.strip():
            tk.messagebox.showwarning("Warning!", "Please enter account name.")
            return
        
        sent = inserting_password(account_name, generated_password)
        if sent:
            self.controller.show_frame(Main)


# class that shows the passwords in the database
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

