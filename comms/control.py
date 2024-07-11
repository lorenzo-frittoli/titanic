import RPi.GPIO as GPIO
from struct import unpack
import serial
from sys import stderr
from time import time

PACKET_LEN = 4

def cap(x, a, b):
    return max(min(x, b), a)

class Motor:
    def __init__(self, enable_pin: int, a_pin: int, b_pin: int):
        GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(a_pin, GPIO.OUT)
        GPIO.setup(b_pin, GPIO.OUT)
        GPIO.output(a_pin, 0)
        GPIO.output(b_pin, 0)
        self.pwm = GPIO.PWM(enable_pin, 1000)
        self.pwm.start(0)
        self.a_pin = a_pin
        self.b_pin = b_pin

    def hard_stop(self):
        GPIO.output(self.a_pin, 0)
        GPIO.output(self.b_pin, 0)
        self.pwm.ChangeDutyCycle(100)

    # power from -100 to 100
    def run(self, power: int):
        if abs(power) > 100:
            power = 0
            print(f"{time()}: power = {power}", file=stderr)

        if power >= 0:
            GPIO.output(self.a_pin, 1)
            GPIO.output(self.b_pin, 0)
        else:
            GPIO.output(self.a_pin, 0)
            GPIO.output(self.b_pin, 1)
        self.pwm.ChangeDutyCycle(abs(power))


GPIO.setmode(GPIO.BOARD)
L_motor = Motor(3, 5, 7) # TODO
R_motor = Motor(8, 10, 12) # TODO
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Send data to the arduino via usb
def set_depth(depth: int):
    ser.write(bytes(f"\n{depth}\n", encoding="ascii"))

def update(data: bytes):
    # Unpack data from the socket
    data = unpack("bbh", data)
    print(data)
    L_motor.run(data[0])
    R_motor.run(data[1])
    set_depth(data[2])

def cleanup():
    GPIO.cleanup()
    set_depth(-10)
