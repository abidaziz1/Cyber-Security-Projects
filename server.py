import socket
import threading

def handle_client(client_socket, address):
    print(f"[INFO] Connection from {address} has been established.")
    #Receive data from the client (with a buffer size of 1024 bytes)
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break# If no message is received, break out of the loop
            print(f"[INFO] Received from {address}: {data}")
            # Echo the message back to the client
            client_socket.send(f"Server received: {data}".encode('utf-8'))
        except:
            print(f"[INFO] Connection with {address} has been closed.")
            break
    
    # Close the connection with the client
    client_socket.close()
# Main function to start the server
def start_server():
    # Define the server's IP address and port
    server_ip = '127.0.0.1'  # Localhost
    server_port = 12345
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the IP and port
    server_socket.bind((server_ip, server_port))
    
    # Listen for incoming connections (5 clients can queue at a time)
    server_socket.listen(5)
    print(f"[INFO] Server listening on {server_ip}:{server_port}")
    
    # Accept incoming connections in an infinite loop
    while True:
        client_socket, client_address = server_socket.accept()  # Accept a new connection
        print(f"[INFO] Accepted connection from {client_address}")
        
        # Handle the connection using a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()  # Run the server
