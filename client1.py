import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Receive message from the server
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Server: {message}")
            else:
                # If no message, server has disconnected
                print("Server disconnected")
                client_socket.close()
                break
        except ConnectionResetError:
            print("Server disconnected abruptly")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input("You: ")
        client_socket.send(message.encode('utf-8'))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9000))
    print("Connected to the server.")

    # Start a thread to handle incoming messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Handle sending messages to the server
    send_messages(client_socket)

if __name__ == "__main__":
    start_client()
