import random
import string
import bcrypt
import re
from cs50 import SQL
import sys
import readchar
from cryptography.fernet import Fernet

# conecction with the database sqlite3 from cs50
db = SQL("sqlite:///instance/project.db")

# declaration of global variables for knowing the current session state and user id
session = False
session_id = ""

# main function


def main():
    homepage()

# Password function to mask password input with asterisks


def password_prompt(prompt='Password: '):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        ch = readchar.readchar()
        tch = ch.encode(encoding="UTF-8")
        if tch == b'\n' or tch == b'\r':
            break
        elif tch == b'\b' or tch == b'\x7f':
            print("\b \b", end='', flush=True)
            password = password[0:len(password)-1]
        elif tch == b'\x03':
            print("")
            return
        else:
            password += ch
            print('*', end='', flush=True)
    print("")
    return password

# Logion function wich check the user email and password and if they are correct change the session and session_id variables


def login():
    global session
    global session_id
    print(f"\nLOGIN\n")
    while True:
        try:
            email = input("Email: ")
            if mail_format(email):
                pass
            else:
                continue
            if mail_checker(email):
                pass
            else:
                print("Email not registered.")
                continue
            password = password_prompt()
            if password == None:
                return
            password = password.encode("utf-8")
            user_password = db.execute(
                "SELECT password FROM users WHERE email = ?", email
            )[0]["password"]
            if bcrypt.checkpw(password, user_password):
                session_id = db.execute(
                    "SELECT id FROM users WHERE email = ?", email)[0]['id']
                session = True
                return
            else:
                print("Wrong password.")
                continue
        except KeyboardInterrupt:
            print("\n")
            return

# Register function registers and log new users by creation a register of their mail and password on the users db


def register():
    global session
    global session_id
    print(f"\nREGISTER\n")
    while True:
        try:
            password_validator = False
            email = input("Email: ")
            if mail_format(email):
                if mail_checker(email):
                    print("Email already in use.")
                    continue
                else:
                    pass
                while password_validator == False:
                    password = password_prompt()
                    if password == None:
                        return
                    password_validator = password_checker(password)
                confirmation = password_prompt("Password-Confirmation: ")
                if confirmation == None:
                    return
                if password == confirmation:
                    password, salt = hash(password)
                    db.execute(
                        "INSERT INTO users (email, password, salt) VALUES (?,?,?)",
                        email,
                        password,
                        salt,
                    )
                    session_id = db.execute(
                        "SELECT id FROM users WHERE email = ?", email
                    )[0]['id']
                    db.execute(
                        f"INSERT INTO 'passwords' (id) VALUES({session_id})")
                    print("User creation successfull!")
                    session = True
                    return
                else:
                    print("Confirmation password is wrong.")
            else:
                pass
        except KeyboardInterrupt:
            print("\n")
            return

# function for checking mail format through re


def mail_format(email):
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return True
    else:
        print("Invalid email input. Example: user@domain.tld")
        return False

# function for checking te existence of the user mail on the users db


def mail_checker(email):
    try:
        db.execute("SELECT email FROM users WHERE email = ?", email)[
            0]["email"]
        return True
    except:
        return False

# funcion for checking the password structure for safety passwords


def password_checker(password):
    check = 0
    if len(password) < 8:
        print("The password must be at least 8 characters long.")
        return False
    if not re.search(r"[a-z]", password):
        check += 1
    if not re.search(r"[A-Z]", password):
        check += 1
    if not re.search(r"[0-9]", password):
        check += 1
    if not re.search(r"[$_@]", password):
        check += 1
    if re.search(r"\s", password):
        check += 1
    if check != 0:
        print(
            "Remember, passwords must have at least one lower, one upper, a digit and a valid special character, and must not have spaces"
        )
        return False
    else:
        return True

# hashing function to hash all users password and get them to be more secure


def hash(value):
    bytes = value.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash, salt

# function wich create randomized passwords with a given lenght


def create_password():
    if login_check():
        punctuation = list(string.punctuation)
        digits = list(string.digits)
        lower = list(string.ascii_lowercase)
        upper = list(string.ascii_uppercase)
        random.shuffle(punctuation)
        random.shuffle(digits)
        random.shuffle(lower)
        random.shuffle(upper)
        while True:
            try:
                lenght = int(
                    input("What's the lenght you want for the password? "))
                if lenght >= 8:
                    break
                else:
                    print("Your new password should be at least 8 characters long.")
            except KeyboardInterrupt:
                return
            except:
                print("Please, int numbers only.")

        first_half = round(lenght * (30 / 100))
        second_half = round(lenght * (20 / 100))
        pre_password = []

        for _ in range(first_half):
            pre_password.append(lower[_])
            pre_password.append(upper[_])
        for _ in range(second_half):
            pre_password.append(punctuation[_])
            pre_password.append(digits[_])
        random.shuffle(pre_password)
        password = "".join(pre_password)
        print(f"Perfect, your new password is: {password}")
        return password

# homepage function wich contains the selection screen of the base capabilities of the project


def homepage():
    global session
    global session_id
    while session == False:
        print(
            f"\nWelcome to the password generator and manager!\n\n-Option 1: Login\n-Option 2: Register\n-Option 3: Exit\n\nREMEMBER YOU CAN EXIT FROM ANYTHING BY USING CTRL + C\n"
        )
        try:
            match int(input("Select an option: ")):
                case 1:
                    login()
                    if session_id != "":
                        menu()
                case 2:
                    register()
                    if session_id != "":
                        menu()
                case 3:
                    sys.exit("Thank you, for using us")
                case _:
                    print(f"\n\nRemember the options are 1-3.")
        except KeyboardInterrupt:
            sys.exit(f"\nThank you, for using us")
        except ValueError:
            pass

# menu function wich contains the options for the logged users


def menu():
    global session
    global session_id
    while session == True:
        print(
            f"\nPassword generator and manager!\n\n-Option 1: Generate/Update Password/s\n-Option 2: Get Password/s\n-Option 3: Change My Password/s\n-Option 4: Log out\n\nREMEMBER YOU CAN EXIT FROM ANYTHING BY USING CTRL + C\n"
        )
        try:
            match int(input("Select an option: ")):
                case 1:
                    generate_passwords()
                case 2:
                    get_passwords()
                case 3:
                    update_user_password()
                case 4:
                    print("Log out\n")
                    session_id = ""
                    session = False
                    return
                case _:
                    print(f"\n\nRemember the options are 1-3.")
        except KeyboardInterrupt:
            return
        except ValueError:
            pass

# function for the user password update


def update_user_password():
    print(f"\nUpdate your password\n")
    global session_id
    while True:
        try:
            password = password_prompt()
            if password == None:
                return
            password_test = password.encode("utf-8")
            user_password = db.execute("SELECT password FROM users WHERE id = ?", session_id
                                       )[0]["password"]
            if bcrypt.checkpw(password_test, user_password):
                print("Your new password cannot be the same as the old one.\n")
                continue
            confirmation = password_prompt("Password-Confirmation: ")
            if confirmation == None:
                return
            if password == confirmation:
                password, salt = hash(password)
                db.execute(
                    "UPDATE users SET password = ?, salt = ? WHERE id = ?",
                    password,
                    salt,
                    session_id,
                )
                print("Password Update Successfully!")
                return
            else:
                print("Confirmation password is wrong.")
        except KeyboardInterrupt:
            print("\n")
            return

# function wich help the user to get a new safe password for a desire site


def generate_passwords():
    global session
    global session_id
    while session == True:
        print(f"\nPassword generator\n")
        try:
            site = input(
                "Please introduce the name of the site the password is going to be created for: "
            )
            if len(site.split()) > 1 or len(site.split()) < 1:
                print("The site name must be one word.")
                continue
            sites, keys = get_columns()
            site = site.split()[0].lower().capitalize()
            p_key = site.split()[0].lower().capitalize() + "_key"
            if site.split()[0] in sites:
                if (db.execute(f"SELECT {site} FROM 'passwords' WHERE id = {session_id}")[0][site]) == "" or (db.execute(f"SELECT {site} FROM 'passwords' WHERE id = {session_id}")[0][site]) == None:
                    password = create_password()
                    key = Fernet.generate_key()
                    fernet = Fernet(key)
                    enc_password = fernet.encrypt(password.encode())
                    db.execute(f"UPDATE 'passwords' SET {site} = ?, {p_key} = ? WHERE id = {session_id}", enc_password, key
                               )
                    return
                else:
                    while True:
                        try:
                            answer = input(f"You already have a password for {site}; do you want to update it? (Y/N)"
                                           )
                            if answer.lower() in ["y", "yes"]:
                                password = create_password()
                                key = Fernet.generate_key()
                                fernet = Fernet(key)
                                enc_password = fernet.encrypt(
                                    password.encode())
                                db.execute(
                                    "UPDATE passwords SET ? = ?, ? = ? WHERE id = ?",
                                    site,
                                    enc_password,
                                    p_key,
                                    key,
                                    session_id,
                                )
                                return
                            elif answer.lower() in ["no", "n"]:
                                return
                            else:
                                print("The answer must be Yes/Y or No/N.")
                                continue
                        except:
                            print("The answer must be Yes/Y or No/N.")
                            continue

            else:
                password = create_password()
                key = Fernet.generate_key()
                fernet = Fernet(key)
                enc_password = fernet.encrypt(password.encode())
                db.execute(f"ALTER TABLE 'passwords' ADD '{site}' TEXT")
                db.execute(f"ALTER TABLE 'passwords' ADD '{p_key}' TEXT")
                db.execute(f"Update 'passwords' SET {site} = ?, {p_key} = ? WHERE id = {session_id}",
                           enc_password,
                           key,
                           )
                return

        except KeyboardInterrupt:
            print("\n")
            return

# function wich works as a query of all the user passwords decrypting them with their respective keys


def get_passwords():
    if login_check():
        global session_id
        print(f"\nYour Passwords are:\n")
        sites, keys = get_columns()
        for site, key in zip(sites, keys):
            if db.execute(
                f"SELECT {site},{key} FROM 'passwords' WHERE id = {
                    session_id} AND {site} != ''"
            ):
                db_password = db.execute(
                    f"SELECT {site},{key} FROM 'passwords' WHERE id = {
                        session_id} AND {site} != ''"
                )[0][site]
                db_key = db.execute(
                    f"SELECT {site},{key} FROM 'passwords' WHERE id = {
                        session_id} AND {site} != ''"
                )[0][key]
                fernet = Fernet(db_key)
                password = fernet.decrypt(db_password).decode()
                print(f"{site}: {password}")
        print("\n")

# function for getting all the database columns names


def get_columns():
    if login_check():
        sites = []
        keys = []
        columns = db.execute(
            "SELECT name FROM pragma_table_info('passwords');")
        for column in columns:
            if column["name"] != "id":
                if "_key" in column["name"]:
                    keys.append(column["name"])
                else:
                    sites.append(column["name"])
        return sites, keys

# checker of the login state of the user


def login_check():
    global session
    if session == True:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
