import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1)  # Receive 1 byte at a time
        if not data:
            break  # Exit loop on connection close
        received_char = data.decode()
        print('Received character:', received_char)
