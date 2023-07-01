import RPi.GPIO as GPIO
import time

channel = 25

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor on


def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor off


if __name__ == '__main__':
    try:
#        motor_on(channel)
        motor_off(channel)
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
