import threading
import select

class MessageHandler:
    def __init__(self, peer):
        self.peer = peer

    def start(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            readable, _, _ = select.select([self.peer.socket], [], [], 0.1)
            for sock in readable:
                if sock == self.peer.socket:
                    client, address = sock.accept()
                    threading.Thread(target=self.peer.handle_client, args=(client, address), daemon=True).start()
