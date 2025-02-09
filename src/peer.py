import socket
import threading
from .message_handler import MessageHandler
from .utils import get_local_ip

class Peer:
    def __init__(self):
        self.name = input("Enter your name: ")
        self.port = int(input("Enter your port number: "))
        self.ip = get_local_ip()
        self.peers = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        self.message_handler = MessageHandler(self)

    def run(self):
        print(f"Server listening on port {self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()
        self.message_handler.start()
        self.menu()

    def accept_connections(self):
        while True:
            client, address = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(client, address), daemon=True).start()

    def handle_client(self, client, address):
        while True:
            try:
                message = client.recv(1024).decode('utf-8').strip()
                if not message:
                    continue
                if message == "exit":
                    self.remove_peer(address)
                    break
                print(f"\nReceived from {address}: {message}")
            except:
                self.remove_peer(address)
                break
        client.close()

    def send_message(self, ip, port, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(message.encode('utf-8'))
            print(f"Message sent to {ip}:{port}")
            self.add_peer(ip, port)
        except:
            print(f"Failed to send message to {ip}:{port}")

    def add_peer(self, ip, port):
        self.peers[(ip, port)] = True

    def remove_peer(self, address):
        if address in self.peers:
            del self.peers[address]
            print(f"Peer {address} disconnected")

    def query_peers(self):
        if not self.peers:
            print("No connected peers")
        else:
            print("Connected Peers:")
            for i, (ip, port) in enumerate(self.peers.keys(), 1):
                print(f"{i}. {ip}:{port}")

    def menu(self):
        while True:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query connected peers")
            print("0. Quit")
            choice = input("Enter choice: ")

            if choice == '1':
                ip = input("Enter the recipient's IP address: ")
                port = int(input("Enter the recipient's port number: "))
                message = input("Enter your message: ")
                self.send_message(ip, port, message)
            elif choice == '2':
                self.query_peers()
            elif choice == '0':
                print("Exiting")
                break
            else:
                print("Invalid choice. Please try again.")
