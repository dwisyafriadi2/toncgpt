from cryptography.fernet import Fernet

# Generate a key and save it
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key to a file
with open('config.key', 'wb') as key_file:
    key_file.write(key)

# Read the code from the file you want to encrypt
with open('play.py', 'rb') as file:
    code = file.read()

# Encrypt the code
encrypted_code = cipher_suite.encrypt(code)

# Save the encrypted code to a new file
with open('data.py', 'wb') as enc_file:
    enc_file.write(encrypted_code)

print("Code in play.py has been encrypted and saved as encrypted_play.py.")
print("Encryption key saved as key.key.")
