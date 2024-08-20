import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Client: {message}")
            else:
                # If no message, client has disconnected
                print("Client disconnected")
                client_socket.close()
                break
        except ConnectionResetError:
            print("Client disconnected abruptly")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9000))
    server_socket.listen(1)
    print("Server is listening on port 9000...")
    
    client_socket, client_address = server_socket.accept()
    print(f"Client {client_address} connected.")

    # Start a thread to handle incoming messages from the client
    receive_thread = threading.Thread(target=handle_client, args=(client_socket,))
    receive_thread.start()

    # Handle sending messages to the client
    send_messages(client_socket)

if __name__ == "__main__":
    start_server()
