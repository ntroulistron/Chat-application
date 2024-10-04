import socket
import ssl
import threading
import sys
import os
import logging
import json
from cryptography.fernet import Fernet

# Basic logging configuration
logging.basicConfig(level=logging.DEBUG)

class P2PClient:
    # Initialization of the P2PClient class
    def __init__(self):
        # SSL context for encrypted connections
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        # Client socket and SSL client initialization
        self.ssl_client = None
        self.client_socket = None

        # Flag to check if the client is logged in
        self.logged_in = False

        # Symmetric key for encryption/decryption
        self.symmetric_key = None

        # List of known peer addresses
        self.peers = []

    # Logs client actions into a file in an encrypted format
    def log_client_action(self, action):
        filename = "actions_log.txt"
        encrypted_action = Fernet(self.symmetric_key).encrypt(action.encode())
        with open(filename, "ab") as file:
            file.write(encrypted_action + b'\n')

    # Updates the list of peers known to the client
    def update_peers(self, new_peer):
        if new_peer not in self.peers:
            self.peers.append(new_peer)
            print("Updated peers list:", self.peers)

    # Establishes a connection to a peer
    def connect_to_peer(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((host, port))
            print(f"Connected to peer at {host}:{port}")

            # Receiving and updating the list of peers from the connected peer
            peers_data = self.client_socket.recv(1024).decode()
            self.peers = json.loads(peers_data)
            print("Received list of peers:", self.peers)

        except Exception as e:
            print(f"Error connecting to peer: {e}")

    # Connects to the chat server
    def connect_to_server(self, host, port):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.ssl_client = self.ssl_context.wrap_socket(self.client_socket, server_hostname=host)
            print("Connected to the server.")
        except Exception as e:
            print(f"Error connecting to the server: {e}")
            sys.exit(1)

    # Handles the login process
    def login(self):
        try:
            # Receive and decode the symmetric key from the server
            self.symmetric_key = self.ssl_client.recv(2048).decode()
            fernet = Fernet(self.symmetric_key)

            attempts = 0
            while attempts < 3:
                # Prompt user for credentials
                username = input("Enter your username: ")
                password = input("Enter your password: ")

                # Encrypt and send credentials to the server
                encrypted_credentials = fernet.encrypt(f"{username}~{password}".encode())
                self.ssl_client.sendall(encrypted_credentials)

                # Receive and decrypt server's response
                server_response_encrypted = self.ssl_client.recv(2048)
                server_response = fernet.decrypt(server_response_encrypted).decode("utf-8")

                # Check server's response for authentication status
                if server_response == "Authentication successful":
                    print("Logged in successfully. You can start chatting now!")
                    self.logged_in = True
                    return
                elif server_response == "Verification failed":
                    print("Login failed. Please try again.")
                    attempts += 1

            # Handle exceeding the maximum login attempts
            print("Failed to log in after 3 attempts. Exiting.")
            self.ssl_client.close()
            sys.exit(1)

        except Exception as e:
            print(f"Error during login: {e}")
            self.ssl_client.close()

    # Sends a message to the server
    def send_message(self, message):
        if self.ssl_client:
            try:
                # Encrypt and send the message
                fernet = Fernet(self.symmetric_key)
                encrypted_message = fernet.encrypt(message.encode())
                self.ssl_client.sendall(encrypted_message)
                self.log_client_action(f"Message sent: {message}")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("Error: Not connected to the server.")

    # Sends a direct message to a specific recipient
    def send_direct_message(self, recipient, message):
        if self.logged_in:
            # Format and send the direct message
            direct_message = f"/msg {recipient} {message}"
            self.send_message(direct_message)
        else:
            print("Error: Not logged in.")

    # Receives and decrypts messages from the server
    def receive_messages(self):
        try:
            while self.ssl_client:
                encrypted_message = self.ssl_client.recv(2048)
                if not encrypted_message:
                    break
                fernet = Fernet(self.symmetric_key)
                decrypted_message = fernet.decrypt(encrypted_message).decode()
                print(decrypted_message)
        except ConnectionResetError as cre:
            print("Connection with the server was reset.")
        except Exception as e:
            print(f"Error receiving message: {e}")
        finally:
            if self.ssl_client:
                self.ssl_client.close()

# Main execution block
if __name__ == "__main__":
    client = P2PClient()
    host = input("Enter host IP to connect to: ")
    port = int(input("Enter port: "))

    # Establishing connection to the server
    client.connect_to_server(host, port)

    # Handling the login process
    client.login()

    # Manually updating the peers list for testing purposes
    new_peer = ('127.0.0.2', 12345)
    client.update_peers(new_peer)

    # Main chat loop
    if client.logged_in:
        client.log_client_action(f"User logged in")
        receive_thread = threading.Thread(target=client.receive_messages, daemon=True)
        receive_thread.start()

        while client.logged_in:
            message = input("Enter a message (or '/msg username message' for direct message, 'exit' to quit): ")
            if message.lower() == "exit":
                break
            if message.startswith('/msg'):
                _, recipient, msg_body = message.split(' ', 2)
                client.send_direct_message(recipient, msg_body)
            else:
                client.send_message(message)

        client.ssl_client.close()
