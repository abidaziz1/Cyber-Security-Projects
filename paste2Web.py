import requests  # For sending and receiving HTTP requests
import re  # For regex operations
import base64  # For encoding and decoding messages
import random  # For generating random strings
import string  # For string manipulation
import os  # For clearing the terminal screen
from cryptography.fernet import Fernet  # For encryption and decryption

# Function to clear the terminal screen
def clear():
    if os.name == "nt":  # Check if the OS is Windows
        os.system("cls")  # Clear screen for Windows
    else:
        os.system("clear")  # Clear screen for Unix/Linux

# Function to generate a random word used in URLs
def rand():
    word = ""
    for _ in range(30):  # Generate a random string of 30 characters
        word += random.choice(string.ascii_letters + string.digits)
    return word

# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()  # Generate and return a Fernet encryption key

# Function to encrypt a message using a key
def encrypt_message(message, key):
    fernet = Fernet(key)  # Create a Fernet cipher object
    encrypted_message = fernet.encrypt(message.encode())  # Encrypt the message
    return encrypted_message.decode()  # Return the encrypted message as a string

# Function to decrypt a message using a key
def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)  # Create a Fernet cipher object
    decrypted_message = fernet.decrypt(encrypted_message.encode())  # Decrypt the message
    return decrypted_message.decode()  # Return the decrypted message as a string

# Function to send a list of messages to cl1p.net
def send(msgs, encryption_key=None):
    word = rand()  # Generate a random word for the URL
    print("Today's word is:", word)
    print("-" * 10)
    n = 0
    for msg in msgs:
        msg = msg.replace("\r", "").replace("\n", "<(!NeWLIne!)>")  # Replace newline characters
        if encryption_key:  # Encrypt the message if an encryption key is provided
            msg = encrypt_message(msg, encryption_key)
        word_with_index = word[:30] + str(n)  # Append the index to the random word
        link = f"https://cl1p.net/{word_with_index}"  # Construct the URL
        try:
            # Send the message to the URL, encoded in Base64
            requests.post(link, data={"content": base64.b64encode(msg.encode("utf-8"))})
            print(f"[ Part {n} Sent ]")  # Print a success message
        except requests.exceptions.RequestException as e:  # Handle request exceptions
            print(f"Failed to send part {n}: {e}")
        n += 1
    print("-" * 10)
    print("Today's key is:", str(n ** 2 ** 2))  # Print the key for receiving the message

# Function to receive messages from cl1p.net
def receive(word, key, encryption_key=None):
    print("Receiving..")
    print("-" * 5 + "Message" + "-" * 5)
    regex = re.compile(r'tent">(.*)</')  # Regex to extract the message content
    key = int(pow(pow(int(key), 0.5), 0.5))  # Convert the key back to its original form
    for i in range(key):
        word_with_index = word[:30] + str(i)  # Append the index to the word
        link = f"https://cl1p.net/{word_with_index}"  # Construct the URL
        try:
            source = requests.get(link).text  # Get the content of the URL
            msg = regex.findall(source)[0]  # Extract the message content using regex
            msg = base64.b64decode(msg.encode("utf-8")).decode("utf-8")  # Decode the Base64 message
            if encryption_key:  # Decrypt the message if an encryption key is provided
                msg = decrypt_message(msg, encryption_key)
            msg = msg.replace("<(!NeWLIne!)>", "\n")  # Replace placeholders with newlines
            print(msg, end=" ")  # Print the message
        except (requests.exceptions.RequestException, IndexError) as e:  # Handle errors
            print(f"Failed to receive part {i}: {e}")
    print("\r" + "-" * 5 + "Message" + "-" * 5)

# Main function to interact with the user
def main():
    clear()  # Clear the terminal screen
    print('\n --  ---  ---WELCOME BACK---  --   --   -- -')
    print(" --Paste2web-  --   --  --Secret messages---")
    print(" - -Do you want to (S)end or (R)eceive? - -")
    put = input("(S-R)>> ").lower()  # Prompt the user to send or receive a message

    encryption_key = None
    use_encryption = input("Do you want to use encryption? (Y/N) >> ").lower()  # Ask if encryption should be used
    if use_encryption == 'y':
        encryption_key = generate_key()  # Generate an encryption key
        print("Your encryption key is:", encryption_key.decode())  # Display the encryption key

    if put == "s":
        print("Type <(Done)> alone on a line when you finish the message\n..\n")
        final_msg = ""
        while True:
            x = input()
            if x.lower() != "<(done)>":
                final_msg += x + "\n"  # Add the input to the message
            else:
                print("\n..")
                break
        print("\nSending..")
        try:
            send(final_msg.split(" "), encryption_key)  # Split the message and send it
            print("Sent!")
        except Exception as e:
            print("!" * 10 + f"-ERROR SENDING MESSAGE- {e}" + "!" * 10)
        exit(0)

    elif put == "r":
        word = input("Today's word is: ")
        key = input("Today's key is: ")
        if use_encryption == 'y':
            encryption_key = input("Enter the encryption key: ").encode()  # Prompt for the encryption key
        receive(word, key, encryption_key)  # Receive the message
        exit(0)
    else:
        main()  # Restart the process if the input is invalid

# Entry point of the script
if __name__ == '__main__':
    main()  # Call the main function to start the script
