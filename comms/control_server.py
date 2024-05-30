import socket
import keyboard

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 5000        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            event = keyboard.read_event()
            if event.name not in "wasdqe":
                continue
            conn.sendall(event.name.encode())  # Send user input as bytes
