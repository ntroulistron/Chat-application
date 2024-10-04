import socket
import threading
import ssl
import os
import logging
import json
from cryptography.fernet import Fernet

# Basic logging configuration
logging.basicConfig(level=logging.DEBUG)

# Server configuration
HOST = "127.0.0.1"  # Localhost
PORT = 12345        # Port number for the server
LISTENER_LIMIT = 5  # Limit for the number of incoming connections

# Dictionary to keep track of connected clients (username, socket pairs)
connected_clients = {}

# Generate a Fernet key for encryption
fernet_key = Fernet.generate_key().decode() 

# Function to log server actions
def log_server_action(action):
    """Logs server actions both to a file and to the console."""
    filename = "actions_log.txt"
    encrypted_action = Fernet(fernet_key.encode()).encrypt(action.encode())
    with open(filename, "ab") as file:
        file.write(encrypted_action + b'\n')
    print(action)  # Print to console for real-time logging

# Function to authenticate clients
def authenticate(client, username, password):
    """Authenticates clients based on username and password."""
    valid_credentials = [
        ("user", "1234"),
        ("admin", "admin1234"),
        ("guest", "guest1234")
    ]

    # Check if provided credentials match any valid pair
    for valid_username, valid_password in valid_credentials:
        if username.strip() == valid_username and password.strip() == valid_password:
            log_server_action(f"Authentication successful for {username}")
            client.sendall(Fernet(fernet_key.encode()).encrypt(b"Authentication successful"))
            return username

    # Log failed attempts and inform the client
    log_server_action(f"Authentication failed for {username}")
    client.sendall(Fernet(fernet_key.encode()).encrypt(b"Verification failed"))
    return None

# Function to broadcast messages to clients
def broadcast(message, sender_username, recipient="all"):
    """Sends a message to all connected clients or a specific recipient."""
    for client_username, client_socket in connected_clients.items():
        if recipient == "all" or recipient == client_username:
            try:
                fernet = Fernet(fernet_key.encode())
                log_server_action(f"Broadcast message from {sender_username}: {message}")
                encrypted_message = fernet.encrypt(f"{sender_username}~{message}".encode())
                client_socket.sendall(encrypted_message)
            except Exception as e:
                print(f"Error broadcasting to {client_username}: {e}")

# Function to handle individual client connections
def handle_client(client, address):
    """Handles the client-server interaction for each connected client."""
    ssl_socket = None
    username = None
    try:
        # Setup SSL for secure communication
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.pem")
        ssl_socket = context.wrap_socket(client, server_side=True)

        # Send the symmetric key to the client
        ssl_socket.sendall(fernet_key.encode())

        # Handle authentication with a maximum of 3 attempts
        authenticated = False
        for attempt in range(3):
            credentials = ssl_socket.recv(2048)
            if not credentials:
                break

            decrypted_credentials = Fernet(fernet_key.encode()).decrypt(credentials).decode()
            username, password = decrypted_credentials.split("~")

            if authenticate(ssl_socket, username, password):
                authenticated = True
                break

        # Close connection if authentication fails
        if not authenticated:
            ssl_socket.sendall(Fernet(fernet_key.encode()).encrypt(b"MaxAttempts"))
            ssl_socket.close()
            return

        # Main loop to receive and broadcast messages
        while True:
            encrypted_message = ssl_socket.recv(2048)
            if not encrypted_message:
                break

            fernet = Fernet(fernet_key.encode())
            message = fernet.decrypt(encrypted_message).decode("utf-8")

            # Handle direct messages or broadcast to all
            if message.startswith('/msg'):
                recipient, msg_body = message.split(' ', 2)[1:]
                send_direct_message(recipient, msg_body, username)
            else:
                print(f"Received message from {username}: {message}")
                broadcast(message, username)

    # Handling disconnections and errors
    except Exception as e:
        print(f"Client {username} disconnected abruptly: {e}")
        if username and username in connected_clients:
            del connected_clients[username]
            log_server_action(f"{username} disconnected")
            broadcast(f"{username} has left the chat.", "Server")
    finally:
        if ssl_socket:
            ssl_socket.close()

# Function to send direct messages to a specific client
def send_direct_message(server, recipient, message, sender_username):
    """Sends a private message to a specific client."""
    if recipient in connected_clients:
        recipient_socket = connected_clients[recipient]
        try:
            fernet = Fernet(fernet_key.encode())
            encrypted_message = fernet.encrypt(f"{sender_username} (private): {message}".encode())
            recipient_socket.sendall(encrypted_message)
        except Exception as e:
            print(f"Error sending direct message to {recipient}: {e}")
    else:
        print(f"{recipient} is not connected.")

# Main function to start the server
def start_server():
    """Starts the server and listens for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen(LISTENER_LIMIT)
        print(f"Server is listening on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        return
    while True:
        client, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, address))
        client_handler.start()

# Execute the server
if __name__ == '__main__':
    start_server()
