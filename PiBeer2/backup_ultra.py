#Libraries
import RPi.GPIO as GPIO
import time
import os
import numpy as np
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
isOn = 0
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

if __name__ == '__main__':
    try:

        with open('distance.cfg') as f:
            contents = f.read()
            print(contents)


        while True:
            dist = distance()
            # round our value for clarity
            dist = np.round(dist,2)
            #  write out the current distance and the set cut off distance.
            print ("Measured Distance = %.1f cm ", dist , "of ", contents )

            # if  the motor is off and the distance is more than  the target - turn on motor..
            if isOn==0 and dist > float(contents):
                isOn=1
                print("light :" , isOn)
                os.system("python3 toggleswon.py")

            # if  the motor is on and the distance is less than the target - turn off motor..
            if isOn==1 and dist < float(contents):
                isOn=0
                print("light :" , isOn)
                os.system("python3 toggleswoff.py")

            # wait half a second and check again
            time.sleep(0.5)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        # if we quit, then  turn off script.
        os.system("python3 toggleswoff.py")
        GPIO.cleanup()
