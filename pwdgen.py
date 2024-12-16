import random
import string

# Function to generate a random password
def generate_password(length=12):
    if length < 6:
        print("Password length should be at least 6 characters.")
        return None
    
    # Characters to include in the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to save a password to the password manager
def save_password(account_name, password):
    with open("passwords.txt", "a") as file:
        file.write(f"{account_name}: {password}\n")
    print(f"Password for '{account_name}' saved successfully.")

# Function to retrieve saved passwords
def retrieve_passwords():
    try:
        with open("randoms.txt", "r") as file:
            print("\nSaved Passwords:")
            print(file.read())
    except FileNotFoundError:
        print("No saved passwords found.")

# Main program
def main():
    print("Welcome to the Password Manager!")
    while True:
        print("\nOptions:")
        print("1. Generate a new password")
        print("2. Save a password")
        print("3. Retrieve saved passwords")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            length = int(input("Enter the password length: "))
            password = generate_password(length)
            if password:
                print(f"Generated Password: {password}")
        
        elif choice == "2":
            account_name = input("Enter the account name: ")
            password = input("Enter the password to save: ")
            save_password(account_name, password)
        
        elif choice == "3":
            retrieve_passwords()
        
        elif choice == "4":
            print("Exiting the Password Manager. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
