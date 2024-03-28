import tkinter as tk
import secrets
import string
import mysql.connector
import tkinter.messagebox
import pyperclip


# class that creates the base of the app
class PasswordGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating main window
        self.title("Password Generator")
        self.geometry("500x400")

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

        if not username.strip():
            tk.messagebox.showwarning("Warning!", "Please enter username.")
            return
        
        if not password.strip():
            tk.messagebox.showwarning("Warning!", "Please enter password.")
            return

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

        title_label = tk.Label(self, text = "Create and Save Password")
        title_label.grid(row = 0, column = 1, pady = 3)

        # function to re generate password
        def regenarate_password():
            self.password = generate_password()
            displaying_password.config(text = self.password)

        # generated password related widgets
        generated_password_label = tk.Label(self, text = "Generated Password:  ")
        generated_password_label.grid(row = 1, column = 0, sticky = 'es', pady = 3)

        displaying_password = tk.Label(self, text = self.password)
        displaying_password.grid(row = 1, column = 1, pady = 3)

        regenarate_button = tk.Button(self, text = "Re-Generate", command = regenarate_password)
        regenarate_button.grid(row = 1, column = 2, sticky = 'ws', pady = 3)

        copy_button = tk.Button(self, text = "Copy", command = self.copy_password)
        copy_button.grid(row = 1, column = 3, sticky = 'ws', pady = 3)


        # password related widgets
        password_label = tk.Label(self, text = "Enter Password: ")
        password_label.grid(row = 2, column = 0, pady = 3)

        self.password_field = tk.Entry(self)
        self.password_field.grid(row = 2, column = 1, pady = 3)


        # account name related widgets
        account_label = tk.Label(self, text = "Enter Account Name: ")
        account_label.grid(row = 3, column = 0, sticky = 'es', pady = 3)

        self.account_field = tk.Entry(self)
        self.account_field.grid(row = 3, column = 1, sticky = 's', pady = 3)


        # save and back buttons
        save_button = tk.Button(self, text = "Save", command = self.send_accName_GenPassword)
        save_button.grid(row = 4, column = 1, sticky = 'ws', pady = 3)

        back_button = tk.Button(self, text = "Back", command = self.backToMain)
        back_button.grid(row = 4, column = 1, sticky = 'es', pady = 3)


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)


    # function that sends acc_name and generated_password to inserting_password() 
    def send_accName_GenPassword(self):
        account_name = self.account_field.get()
        generated_password = self.password_field.get()

        if not generated_password.strip():
            tk.messagebox.showwarning("Warning!", "Please enter password.")
            return
        
        if not account_name.strip():
            tk.messagebox.showwarning("Warning!", "Please enter account name.")
            return
        
        # send information to inserting_password()
        sent = inserting_password(account_name, generated_password)
        if sent:
            self.account_field.delete(0, tk.END)
            self.password_field.delete(0, tk.END)
            self.controller.show_frame(Main)
    

    # function to copy password to clipboard
    def copy_password(self):
        pyperclip.copy(self.password)
        tk.messagebox.showinfo("Copied!", "Generated password copied to clipboard.")


    # function for back_button
    def backToMain(self):
        self.account_field.delete(0, tk.END)
        self.password_field.delete(0, tk.END)
        self.controller.show_frame(Main)




# class that shows the passwords in the database
class ViewP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_labels = []
        
        # head title of the page
        title_label = tk.Label(self, text = "Passwords from the database: ")
        title_label.grid(row=0, columnspan=2, sticky='s')

        # frame to display passwords
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, columnspan=3, sticky='n')
        self.passwords_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.passwords_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)


        # 
        account_label = tk.Label(self, text = "Enter Account to Copy Password: ")
        account_label.grid(row=2, column=0,)

        self.account_field = tk.Entry(self)
        self.account_field.grid(row=2, column=1, sticky='ws')

        # Button to copy password
        copy_button = tk.Button(self, text="Copy", command=self.copy_password)
        copy_button.grid(row=2, column=2, sticky='ws')


        # button to go back to the Main page
        back_button = tk.Button(self, text = "Back", command = self.backToMain)
        back_button.grid(row=3, columnspan=2, sticky='s', pady=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

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


    # function to call getting_passwords()
    def getting_passwords(self):
        getting_passwords(self)
    

    # Function to copy password to clipboard
    def copy_password(self):
        # Get account name to copy password
        account_name = self.account_field.get()
        if not account_name.strip():
            tk.messagebox.showwarning("No Account Entered", "Please enter an account name.")
            return

        # Get password from the database
        password = get_password_from_database(account_name)
        if password:
            pyperclip.copy(password)
            tk.messagebox.showinfo("Copy Password", "Password copied to clipboard.")
            self.account_field.delete(0, tk.END)
        else:
            tk.messagebox.showwarning("Account Not Found", f"No password found for account '{account_name}'.")

    
    # function for back_button
    def backToMain(self):
        self.account_field.delete(0, tk.END)
        self.controller.show_frame(Main)

    




# class that edits passwords in the database
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

        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row=2, column=1, padx = 1, pady = 3, sticky='ws')

        regenarate_button = tk.Button(self, text = "Re-Generate", command = regenarate_password)
        regenarate_button.grid(row = 2, column = 2, )

        displaying_password = tk.Label(self,  text = self.password)
        displaying_password.grid(row = 2, column = 3, )

        copy_button = tk.Button(self, text = "Copy", command = self.copy_password)  
        copy_button.grid(row = 2, column = 4, padx = 1, pady = 3, )

        # update and back buttons
        update_button = tk.Button(self, text="Update Password", command = self.send_accName_newPassword)
        update_button.grid(row=3, column=1, padx = 1, pady = 3)

        back_button = tk.Button(self, text="Back", command= self.backToMain)
        back_button.grid(row=3, column=2, padx = 7, pady = 3, sticky='es')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)


    # function that sends acc_name and new_password to edititing_passwords() 
    def send_accName_newPassword(self):
        account_name = self.acc_name_field.get()
        new_password = self.password_entry.get()
        
        if not account_name.strip():
            tk.messagebox.showwarning("Warning!", "Please enter account name.")
            return

        if not new_password.strip():
            tk.messagebox.showwarning("Warning!", "Please enter new password.")
            return
        
    
        # send information to inserting_password()
        sent = editing_passwords(new_password, account_name)
        if sent:
            self.acc_name_field.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.controller.show_frame(Main)

    # function to copy password to clipboard
    def copy_password(self):
        pyperclip.copy(self.password)
        tk.messagebox.showinfo("Copied!", "Generated password copied to clipboard.")


    # function for back_button
    def backToMain(self):
        self.password_entry.delete(0, tk.END)
        self.acc_name_field.delete(0, tk.END)
        self.controller.show_frame(Main)




# class that deletes passwords in the database
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
        delete_button = tk.Button(self, text = "Delete", command = self.send_accName)  
        delete_button.grid(row = 2, sticky = "es",padx = 8, pady = 6 )

        back_button = tk.Button(self, text = "Back", command = self.backToMain)  
        back_button.grid(row = 2, column = 1, sticky = "ws", padx = 8, pady = 6)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)

    
    # function that sends acc_name to deleting_passwords() 
    def send_accName(self):
        account_name = self.acc_name_field.get()

        if not account_name.strip():
            tk.messagebox.showwarning("Warning!", "Please enter account name.")
            return
        
        # send information to inserting_password()
        sent = deleting_passwords(account_name)
        if sent:
            self.acc_name_field.delete(0, tk.END)
            self.controller.show_frame(Main)


    # function for back_button
    def backToMain(self):
        self.acc_name_field.delete(0, tk.END)
        self.controller.show_frame(Main)




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


# function to get password to copy
def get_password_from_database(account_name):
    try:
        # Query to retrieve password from the database based on account name
        cursor.execute("SELECT password FROM GeneratedPasswords WHERE acc_name = %s", (account_name,))
        password_row = cursor.fetchone()
        if password_row:
            return password_row[0]  # Assuming password is in the first column
        else:
            return None
    except mysql.connector.Error as err:
        tk.messagebox.showerror("Database Error", f"Error accessing database: {err}")
        return None  


# editing passwords in the database
def editing_passwords(new_password, account_name):
    try:
        # Check if the account exists in the database
        cursor.execute("SELECT * FROM GeneratedPasswords WHERE acc_name = %s", (account_name,))
        account_row = cursor.fetchone()
        if not account_row:
            tk.messagebox.showwarning("Account Not Found", f"No account named '{account_name}' found in the database.")
            return False
        
        # Update the password for the account
        cursor.execute("UPDATE GeneratedPasswords SET password = %s WHERE acc_name = %s", (new_password, account_name))
        connection.commit()

        tk.messagebox.showinfo("Password Updated", f"Password for account '{account_name}' successfully updated.")
        return True
    
    except mysql.connector.Error as err:
        tk.messagebox.showerror("Database Error", f"Error updating password: {err}")
        return False



# deleting passwords from the database
def deleting_passwords(account_name):
    try:
        # query to delete row from the database
        cursor.execute("delete from GeneratedPasswords where acc_name = %s", (account_name,))
        connection.commit()

        # status message box
        tk.messagebox.showinfo("Delete Status", f"Password for account {account_name} has been removed successfuly.")
        return True
    
    except mysql.connector.Error as err:
        # error alert box
        tk.messagebox.showerror("Error", f"Error: {err}")
        return False
    
    finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()
