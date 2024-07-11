import socket

import control

HOST = "192.168.1.192"  # The server's hostname or IP address
PORT = 5000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connetcting... ")
    s.connect((HOST, PORT))
    print("Connected.")
    try:
        while True:
            # Receive commands
            data = s.recv(control.PACKET_LEN)
            if not data:
                break  # Exit loop on connection close

            control.update(data)

    # break the infinite loop and perform cleanup
    except (KeyboardInterrupt, ConnectionRefusedError, OSError):
        pass

# perform GPIO cleanup
control.cleanup()
