import socket

def run_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))  
        s.listen()
        print(f"Listening on port {port}")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}") 
if __name__ == "__main__":
    port = int(input("Enter the port to listen on: ")) 
    run_server(port)