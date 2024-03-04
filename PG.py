import string
import secrets
import importlib

def generate_password(length=12, uppercase=True, digits=True, special_chars=True):
    characters = string.ascii_lowercase

    if uppercase:
        characters += string.ascii_uppercase
    if digits:
        characters += string.digits
    if special_chars:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password







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