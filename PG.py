import tkinter as tk
import secrets
import string
import mysql.connector
import tkinter.messagebox

# TODO: create functions for deleting and updating passwords
# TODO: create scrolling list   <-(needs some tweaking)->
# TODO: create copy button for ViewP

# TODO (Optional): create page where users can create their own database
# TODO (Optional): think of how can create sign up page

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


# function to create a cursor for mysql queries
def get_cursor():
    if 'connection' in globals() and 'cursor' in globals():
        return cursor
    else:
        return None


# saving passwords to the database
def inserting_password(account_name, generated_password):
    try:
        # query to insert data to the database
        cursor.execute("insert into GeneratedPasswords (acc_name, password) values (%s, %s)", (account_name, generated_password))
        connection.commit()

        # status message box
        tk.messagebox.showinfo("Password Saved Status", "Congradulations, Your password has been saved successfully!")
        return True
    
    except mysql.connector.Error as err:
        # error alert box
        tk.messagebox.showerror("Error", f"Error: {err}")
        return False
    
    finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


# function to get passwords from the database
def getting_passwords(ViewP_instance):

    # getting cursor for mysql queries 
    cursor = get_cursor()

    # if statement to check if cursor is connected (if not that means the user didn't log in)
    if cursor:
        try:
            # mysql query to select all passwords from database
            cursor.execute("select * from GeneratedPasswords")
            passwords_list = cursor.fetchall()

            # for loop to clear the list after left the page
            for label in ViewP_instance.password_labels:
                label.destroy()
            ViewP_instance.password_labels.clear()

            # if statement to check if there are any passwords in the database
            if passwords_list:

                # loop to show passwords if there are any
                for idx, password in enumerate(passwords_list):
                    # displaying id
                    id_label = tk.Label(ViewP_instance.passwords_frame, text = password[0])
                    id_label.grid(row = idx, column =0, padx = 5, pady = 5)
                    ViewP_instance.password_labels.append(id_label)

                    # displaying acc name
                    acc_name_label = tk.Label(ViewP_instance.passwords_frame, text = password[1])
                    acc_name_label.grid(row = idx, column = 1, padx = 5, pady = 5)
                    ViewP_instance.password_labels.append(acc_name_label)

                    # displaying password
                    password_label = tk.Label(ViewP_instance.passwords_frame, text = password[2])
                    password_label.grid(row = idx, column = 2, padx = 5, pady = 5)
                    ViewP_instance.password_labels.append(password_label)
            else:
                # label to show that the are no passwords in the database
                no_passwords_label = tk.Label(ViewP_instance.passwords_frame, text = "No passwords were saved in the database.")
                no_passwords_label.pack()
                ViewP_instance.password_labels.append(no_passwords_label)

        except mysql.connector.Error as err:
            # error alert box
            tk.messagebox.showerror("Error", f"Error: {err}")   
    else:
        # warning box to tell user to log in
        tk.messagebox.showwarning("Warning!", "Please log in first.")


# class that creates the base of the app
class PasswordGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating main window
        self.title("Password Generator")
        self.geometry("600x400")

        self.username = None
        self.password = None

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
        if cont == ViewP:
            if self.username and self.password:
                frame = self.frames[cont]
                frame.getting_passwords()
                frame.tkraise()
        else:
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
        # getting data from fields
        username = self.username_field.get()
        password = self.password_field.get()

        # sending data to database_config()
        success = database_config(username, password)
        
        # if sent then we define those variables and return to main page
        if success:
            self.controller.username = username
            self.controller.password = password
            self.controller.show_frame(Main)
        

# class for main page where you will choose what to do (after login page)
class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = tk.Label(self, text="Welcome to the Password Generator.")
        title.grid(row = 0)
    
        PasswordGeneratorPage = tk.Button(self, text="Generate Password", command=lambda: controller.show_frame(PGpage))
        PasswordGeneratorPage.grid(row = 1, pady =3)

        PasswordViewPage = tk.Button(self, text = "View Passwords", command=lambda: controller.show_frame(ViewP))
        PasswordViewPage.grid(row = 2, pady =3)

        PasswordEditPage = tk.Button(self, text = "Edit Passwords", command = lambda:controller.show_frame(EditP))
        PasswordEditPage.grid(row = 3, pady =3)

        PasswordDeletePage = tk.Button(self, text = "Delete Passwords", command = lambda:controller.show_frame(DeleteP))
        PasswordDeletePage.grid(row = 4, pady =3)

        self.grid_columnconfigure(0, weight=1)


# class for password generating and adding account name (and sending to database)
class PGpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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

        back_button = tk.Button(self, text = "Back", command = self.backToMain)
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
        
        # send information to inserting_password()
        sent = inserting_password(account_name, generated_password)
        if sent:
            self.account_field.delete(0, tk.END)
            self.controller.show_frame(Main)
    
    # function for back_button
    def backToMain(self):
        self.account_field.delete(0, tk.END)
        self.controller.show_frame(Main)


# class that shows the passwords in the database
class ViewP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_labels = []
        
        # head title of the page
        title_label = tk.Label(self, text = "Passwords from the database: ")
        title_label.grid(row=0, columnspan=2)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, columnspan=2)

        # Frame to display passwords
        self.passwords_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.passwords_frame, anchor="nw")

        # Bind mouse wheel events to scroll the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # button to go back to the Main page
        back_button = tk.Button(self, text = "Back", command = lambda:controller.show_frame(Main))
        back_button.grid(row=2, columnspan=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.scroll_pos = 0

    # enable scrolling
    def _on_mousewheel(self, event):
        delta = event.delta

        # check if the canvas is scrollable in the current direction
        if delta < 0:
            # Scroll down if possible
            self.canvas.yview_scroll(1, "units")
        elif delta > 0:
            # Scroll up if possible
            self.canvas.yview_scroll(-1, "units")

    def getting_passwords(self):
        getting_passwords(self)


class EditP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password = generate_password()

        # function to re generate password
        def regenarate_password():
            self.password = generate_password()
            displaying_password.config(text = self.password)
        
        title_label = tk.Label(self, text = "Edit Passwords")
        title_label.grid(row = 0, columnspan=4)

        # account related widgets
        acc_name = tk.Label(self, text="Account Name:")
        acc_name.grid(row=1, column=1, padx = 1, pady = 3, sticky='es')

        self.acc_name_field = tk.Entry(self)
        self.acc_name_field.grid(row=1, column=2, padx = 1, pady = 3, sticky='ws')
        
        # password related widgets
        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=2, column=0, padx = 1, pady = 3, sticky='es')

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx = 1, pady = 3, sticky='ws')

        regenarate_button = tk.Button(self, text = "Re-Generate", command = regenarate_password)
        regenarate_button.grid(row = 2, column = 2, )

        displaying_password = tk.Label(self,  text = self.password)
        displaying_password.grid(row = 2, column = 3, )

        copy_button = tk.Button(self, text = "Copy", command = "smth")  # update command
        copy_button.grid(row = 2, column = 4, padx = 1, pady = 3, )

        # update and back buttons
        update_button = tk.Button(self, text="Update Password")     # updating command
        update_button.grid(row=3, column=1, padx = 1, pady = 3)

        back_button = tk.Button(self, text="Back", command= self.backToMain)
        back_button.grid(row=3, column=2, padx = 7, pady = 3, sticky='es')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)






     # function for back_button
    def backToMain(self):
        self.acc_name_field.delete(0, tk.END)
        self.controller.show_frame(Main)


class DeleteP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text = "Delete Passwords")
        title_label.grid(row = 0, columnspan=2, pady = 10)

        # acc_name widgets
        acc_name_label = tk.Label(self, text = "Enter Account Name: ")
        acc_name_label.grid(row = 1, sticky = "es")

        self.acc_name_field = tk.Entry(self)
        self.acc_name_field.grid(row = 1, column = 1, sticky = "ws")

        # delete and back buttons
        delete_button = tk.Button(self, text = "Delete", command = "smth")  #edit command
        delete_button.grid(row = 2, sticky = "es",padx = 8, pady = 6 )

        back_button = tk.Button(self, text = "Back", command = self.backToMain)  # edit command
        back_button.grid(row = 2, column = 1, sticky = "ws", padx = 8, pady = 6)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)

    # function for back_button
    def backToMain(self):
        self.acc_name_field.delete(0, tk.END)
        self.controller.show_frame(Main)



if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()
