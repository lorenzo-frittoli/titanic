import RPi.GPIO as GPIO
import time

ENABLE = 11
DIRA = 13
DIRB = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.setup(DIRA, GPIO.OUT)
GPIO.setup(DIRB, GPIO.OUT)


GPIO.output(ENABLE, GPIO.HIGH)
GPIO.output(DIRA, GPIO.LOW)
GPIO.output(DIRB, GPIO.HIGH)

time.sleep(20)

GPIO.cleanup()
