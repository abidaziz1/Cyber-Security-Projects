import socket  # Import the socket module to create network connections

# Main function to start the client
def start_client():
    # Define the server's IP address and port (same as in the server)
    server_ip = '127.0.0.1'  # Localhost
    server_port = 12345
    
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"[INFO] Connected to server at {server_ip}:{server_port}")
        
        # Send and receive messages in an infinite loop
        while True:
            # Input message to send to the server
            message = input("You: ")
            
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
            
            # Receive a response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server: {response}")
            
            # Exit loop if user types 'exit'
            if message.lower() == 'exit':
                print("[INFO] Closing connection to the server.")
                break
    except ConnectionRefusedError:
        print("[ERROR] Connection failed. Make sure the server is running.")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_client()  # Run the client
