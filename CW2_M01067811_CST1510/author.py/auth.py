import bcrypt
import os

def hash_password(plaintext_password: str) -> str:
#Encoding password to bytes
    password_bytes = plaintext_password.encode('utf-8')
#Generating a salt for the password
    salt = bcrypt.gensalt()
#Hashing the password with the generated salt
    hashed = bcrypt.hashpw(password_bytes, salt)
#Decoding the hash to string and returning it
    return hashed.decode('utf-8')

def verify_password(plaintext_password: str, hashed_password: str) -> bool:
#Encoding plaintext password to bytes
    plaintext_bytes = plaintext_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Verifying if the plaintext password matches the hash password
    return bcrypt.checkpw(plaintext_bytes, hashed_bytes)
    
#Temporary testing code
test_password="Ftaso009!"
#Test hashing the password
hashed_password=hash_password(test_password)
print(f"Original Password: {test_password}")
print(f"Hashed Password: {hashed_password}")
print(f"Hash Length: {len(hashed_password)} characters")
#Test verifying with the correct password
is_correct=verify_password(test_password, hashed_password)
print(f"Verification with correct password: {is_correct}") 
#Test verifying with an incorrect password
is_incorrect=verify_password("WrongPassword123", hashed_password)
print(f"Verification with incorrect password: {is_incorrect}") 
#Defining user data file
user_data_file="users.txt"
#Implementing registration function
def register_user(username, password):
#Checking if username exists
    if user_exists(username):
        print("Username already exists.")
        return False
    else:
        #Hashing the password
        hashed_password=hash_password(password)
        #Adding username and hashed password to the user data file
        with open(user_data_file, "a") as file:
            file.write(f"{username},{hashed_password}\n")
        return True
    
def user_exists(username):
    #Checking if the file exists
    try:
       #Opening the user data file and checking for the username
        with open(user_data_file,"r") as file:
            for line in file:
                #Striping whitespace and splitting by comma
                line_strip=line.strip()
                if username==line_strip.split(",")[0] and line_strip:
                    return True
        return False
    except FileNotFoundError:
        print("User data file not found.")
        return False
    
 #Implementing login function
def login_user(username, password):
    try:
        # Open user data file and look for the username
        with open(user_data_file, "r", encoding='utf-8') as file:
            for line in file:
                line_strip = line.strip()
                if not line_strip:
                    continue
                parts = line_strip.split(',')
                if parts[0] == username and len(parts) >= 2:
                    stored_hash = parts[1]
                    if verify_password(password, stored_hash):
                        return True
        # Not found or verification failed
        return False
    except FileNotFoundError:
        print("User data file not found.")
        return False

def validate_username(username):
   if type(username) != str or len(username) < 5:
       error_msg="Username is not valid must be atleast 5 characters long."
       is_valid= False
       return is_valid, error_msg  
   else:
        error_msg="Username is valid."
        is_valid= True
        return is_valid, error_msg

def validate_password(password):
    if type(password) != str or len(password) < 8:
        error_msg = "Password is not valid: must be at least 8 characters long."
        is_valid = False
        return is_valid, error_msg
    else:
        error_msg="Password is valid."
        is_valid=True
        return is_valid, error_msg
    
    


def display_menu():
    "DISPLAYS THE MENU"
    print("\n"+"="*50)
    print("MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("Secure Authentication System")
    print("="*50)
    print("\n [1] Register")
    print(" [2] Login")
    print(" [3] Exit")
    print("-"*50) 

def main():
    "Main Program Loop"   

    while True:
        display_menu()
        choice=input("Enter your choice (1-3): ").strip()
         
        if choice=="1":
            #Registration process

            username=input("Enter a username: ").strip()
            #Validating username
            is_valid, error_msg=validate_username(username)
            if not is_valid:
                print(f"Error:{error_msg}")
                continue

            password=input("Enter a password: ").strip()
            #Validating password
            is_valid, error_msg=validate_password(password)
            if not is_valid:
                print(f"Error:{error_msg}")
                continue

            #Confirm password
            password_confirm=input("Confirm your password: ").strip()
            if password != password_confirm:
                print("Error: Password dont match.")
                continue
            #Handiling case where username already exists
            if user_exists(username):
                print(f"Error:Username {username} already exists. Please choose a different username.")
                continue

            #Register user
            register_user(username, password)
            print(f"Success:User {username} registered successfully!")
            
        
        elif choice=="2":   
            #Login process
            print("\n--USER LOGIN--")
            username=input("Enter your username: ").strip() 
            password=input("Enter your password: ").strip()

            #Attempt login
            if login_user(username, password):
                print("\nYou are logged in.")
                print(f"Suceess:Welcome , {username}!")
            #Optional:Asking user uf they want to log out
                input ("\nPlease press Enter to return to main menu...")
            
        elif choice=="3":
            #Exit the program
            print("\n Thank you for using the Secure Authentication System. Goodbye!")
            print("Exiting...")
            break
        else:
            print("\nError:Invalid option.Please select 1,2,or 3.")

def check_password_strength(password):
    #Checking for password strength in three categories Weak, Moderate, Strong
    length_criteria=len(password)
    has_upper=any(c.isupper() for c in password)
    has_lower=any(c.islower() for c in password)
    has_digit=any(c.isdigit() for c in password)
    has_special=any(not c.isalnum() for c in password)
    #Weak Password category
    if length_criteria < 6 or has_upper and not(has_lower and has_digit and has_special):
        return "Weak"
    #Strong Password category
    elif (len(password)>=6 and has_upper and has_lower and has_digit and has_special):
        return "Strong"
    #Moderate Password category
    else:  
        return "Moderate"
    
    pass

def register_user_2(username,password,role="user"):
        """Registering a new user with hashed password and role."""
        #Checking if username exists
        if user_exists(username):
            print("Username already exists.")
            return False
        else:
            #Hashing the password
            hashed_password=hash_password(password)
            #Adding username, hashed password, and role to the user data file
            with open(user_data_file,"a") as file:
                file.write(f"{username},{hashed_password},{role}\n")
            return True
        

        
        


















if __name__=="__main__":
    main()
    



