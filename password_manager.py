#password manager

import mysql.connector
from cryptography.fernet import Fernet
#fernet module of the cryptography package has inbuilt functions for the generation of the key, encryption of plaintext into ciphertext, 
#and decryption of ciphertext into plaintext using the encrypt and decrypt methods respectively

# Generate a key for encryption : An encryption key is a random string of bits created explicitly for scrambling and unscrambling data.
def generate_key():
    return Fernet.generate_key()

# Encrypt data 
def encrypt_data(key, data): 
    cipher = Fernet(key) #value of key assigned to a variable
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

# Decrypt data
def decrypt_data(key, encrypted_data):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

# Connect to MySQL
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="swasti21",
        database="pwdmgr"
    )

# Create table for passwords
def create_password_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (id INT(10) AUTO_INCREMENT PRIMARY KEY, password VARCHAR(234));""")

# Insert a new password
# Insert a new password
def insert_password(cursor, username, password, key):
    encrypted_password = encrypt_data(key, password)
    cursor.execute("INSERT INTO passwords (username, password) VALUES (%s, %s)", (username, encrypted_password))


# Retrieve passwords for a given username
def retrieve_passwords(cursor, username, key):
    try:
        cursor.execute("SELECT username, password FROM passwords WHERE username = %s", (username,))
        passwords = cursor.fetchall()
        decrypted_passwords = [(entry[0], decrypt_data(key, entry[1])) for entry in passwords]
        return decrypted_passwords
    except Exception as e:
        print(f"Error retrieving passwords: {e}")
        # Return a default value or handle the error as appropriate for your application
        return []

# Main function
def main():
    key = generate_key()
    connection = connect_to_mysql()
    cursor = connection.cursor()

    create_password_table(cursor)

    while True:
        print("\n1. Store Password")
        print("2. Retrieve Passwords")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            insert_password(cursor, username, password, key)
            connection.commit()
            print("Password stored successfully!")

        elif choice == "2":
            username = input("Enter username: ")
            passwords = retrieve_passwords(cursor, username, key)
            if passwords:
                print("\nStored Passwords:")
                for entry in passwords:
                    print(f"Username: {entry[0]}, Password: {entry[1]}")
            else:
                print("No passwords found for the given username.")

        elif choice == "3":
            break

    cursor.close()
    connection.close()

main()

