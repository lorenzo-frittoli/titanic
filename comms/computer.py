# import libraries
import socket
import struct
import time
from keyboard import is_pressed

def cap(x, a, b):
    return max(min(x, b), a)

HOST = '192.168.1.192'
PORT = 5000        # Port to listen on (non-privileged ports are > 1023)

exit_was_pressed = False
input_enable = True
target_depth_cm = -10.0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Waiting... ")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            print(f"target_depth: {target_depth_cm} cm", end="")
            if is_pressed("p"):
                if not exit_was_pressed:
                    # has just been pressed
                    input_enable = not input_enable
                exit_was_pressed = True
            else:
                exit_was_pressed = False

            target_depth_cm += is_pressed("down") - is_pressed("up") # 10cm / second
            if is_pressed("enter"): # Surface
                target_depth_cm = -10.0

            fw_movement = 100*(is_pressed("w") - is_pressed("s"))
            lat_movement = 100*(is_pressed("d") - is_pressed("a"))

            conn.sendall(struct.pack(
                "bbh",
                cap(round(fw_movement+lat_movement), -100, 100), # left motor
                cap(round(fw_movement-lat_movement), -100, 100), # right motor
                round(target_depth_cm)
            ))
            time.sleep(0.1) # 10hz updates
            print("\r", end="")
