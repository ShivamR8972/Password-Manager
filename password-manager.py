import random
import string
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Load or generate encryption key
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

cipher = Fernet(key)

# Function to generate a random password
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 6:
            messagebox.showerror("Error", "Password length should be at least 6 characters.")
            return
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length.")

# Function to save a password to the password manager
def save_password():
    account_name = account_entry.get()
    password = password_entry.get()
    if not account_name or not password:
        messagebox.showerror("Error", "Account name and password cannot be empty.")
        return
    
    encrypted_password = cipher.encrypt(password.encode())  # Encrypt password
    with open("passwords.txt", "a") as file:
        file.write(f"{account_name}:{encrypted_password.decode()}\n")  # Save as string
    messagebox.showinfo("Success", f"Password for '{account_name}' saved successfully!")
    account_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Function to retrieve saved passwords
def retrieve_passwords():
    try:
        with open("passwords.txt", "r") as file:
            saved_passwords = file.readlines()
        if not saved_passwords:
            messagebox.showinfo("Saved Passwords", "No passwords saved yet.")
            return

        result_window = tk.Toplevel(root)
        result_window.title("Saved Passwords")
        result_text = tk.Text(result_window, wrap=tk.WORD, width=50, height=20)

        for line in saved_passwords:
            account_name, encrypted_password = line.strip().split(":", 1)
            try:
                decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()  # Decrypt password
                result_text.insert(tk.END, f"{account_name}: {decrypted_password}\n")
            except Exception as e:
                result_text.insert(tk.END, f"{account_name}: [Error decrypting password]\n")

        result_text.config(state=tk.DISABLED)
        result_text.pack()
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved passwords found.")

# Main GUI setup
root = tk.Tk()
root.title("Secure Password Manager")

# Input fields and labels
tk.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
length_entry = tk.Entry(root, width=15)
length_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Account Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
account_entry = tk.Entry(root, width=30)
account_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Generated Password:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
password_entry = tk.Entry(root, width=30)
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
generate_btn = tk.Button(root, text="Generate Password", command=generate_password)
generate_btn.grid(row=0, column=2, padx=10, pady=5)

save_btn = tk.Button(root, text="Save Password", command=save_password)
save_btn.grid(row=1, column=2, padx=10, pady=5)

retrieve_btn = tk.Button(root, text="Retrieve Passwords", command=retrieve_passwords)
retrieve_btn.grid(row=2, column=2, padx=10, pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white")
exit_btn.grid(row=3, column=1, pady=10)

# Run the main loop
root.mainloop()
