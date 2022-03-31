# Here I am initializing the pyrebase database for the SprayClock
# in order to check the status of the camera (to detect a person),
# buzzer (to ring alarm), and the load sensor (to sense a person's
# weight on bed) to all be true before accordingly spraying the
# person when the alarm is going off.

# I have explained each function beforehand with comments.
# Thank you for reviewing my code!

import pyrebase
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

IN1 = 7  # GPIO Control Output Pin // GPIO04 (1-wire)
IN2 = 11  # GPIO Control Output Pin // GPIO17
IN3 = 16  # GPIO Control Output Pin // GPIO24
IN4 = 18  # GPIO Control Output Pin // GPIO23

control_pins = [IN1, IN2, IN3, IN4]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Example:
# * Step C0 C1 C2 C3
# *    1  1  0  1  0
# *    2  0  1  1  0
# *    3  0  1  0  1
# *    4  1  0  0  1

halfstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]


# checking that SM(Stepper Motor) is moving in the counterclockwise
# direction for a half rotaion ON (512 steps is full rotation)
def moveSMon():

    print("spraying")
    for i in range(256):  # Stepper Motor to rotate COUNTERCLOCKWISE
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            sleep(0.001)


# checking that SM(Stepper Motor) is moving in the clockwise
# direction for a half rotaion OFF (512 steps is full rotation)
def moveSMoff():
    for i in range(256):  # Stepper Motor to rotate CLOCKWISE
        for halfstep in range(len(halfstep_seq) - 1, -1, -1):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            sleep(0.001)


# initializing pyrebase database
def initDatabase():

    config = {
        "apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
        "authDomain": "sprayclock-4e902.firebaseapp.com",
        "databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
        "storageBucket": "sprayclock-4e902.appspot.com",
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    return db


# ensuring the buzzer(currently sounding alarm),
# camera(detects a person), load sensor(senses a person's weight on bed)
# are all set to true before activating spray
def sprayActivated():

    db = initDatabase()
    ds = "Subsystem Status"

    # checking the Alarm Clock Buzzer value
    myAlarmClockBuzzer = db.child(ds).child("Alarm Clock").child("Buzzer").get()
    # checking the Bed Detection Camera value
    myBedDetectionCamera = db.child(ds).child("Bed Detection").child("Camera").get()
    # checking the Bed Detection Load Sensor value
    myBedDetectionLoadSensor = (
        db.child(ds).child("Bed Detection").child("Load Sensor").get()
    )

    # if the Alarm Clock Buzzer is currently ringing
    if myAlarmClockBuzzer.val() is True:
        # if someone is sensed by the camera to be on the Bed Detection System
        if myBedDetectionCamera.val() is True:
            # if someone is sensed by the load sensor to be on the Bed Detection System
            if myBedDetectionLoadSensor.val() is True:

                # then activate the Spray using the stepper motor
                db.child(ds).child("Spray").child("Stepper Motor").set(
                    True
                )  # DATA FORMAT True (Boolean)

                moveSMon()

                print("spray now activated")
                return True  # The spray is activated
    print("spray still deactivated")
    return False  # The spray is deactivated


# ensuring the button(has been pressed) is set to true and then setting the
# stepper motor(turning off the spray),the buzzer(stopping the alarm), and the
# button(since the true has already been logged) to false before
# deactivating spray
def sprayDeactivated():

    print("sprayD")

    db = initDatabase()
    ds = "Subsystem Status"

    # checking the Alarm Clock Button value
    myAlarmClockButton = db.child(ds).child("Alarm Clock").child("Button").get()

    print(myAlarmClockButton)
    if myAlarmClockButton.val() is True:
        # then deactivate the Spray using the stepper motor
        db.child(ds).child("Spray").child("Stepper Motor").set(
            False
        )  # DATA FORMAT False (Boolean)
        db.child(ds).child("Alarm Clock").child("Buzzer").set(
            False
        )  # THIS IS NOT THE JOB OF THE SPRAY !!!
        db.child(ds).child("Alarm Clock").child("Button").set(
            False
        )  # THIS IS NOT THE JOB OF THE SPRAY !!!

        moveSMoff()

        print("spray now deactivated")
        return False
    print("spray still activated")
    return True


def main():
    try:
        print("main")
        sprayState = sprayActivated()

        while True:  # infinite loop, therefore, constantly checking
            if sprayState is True:
                sprayState = sprayDeactivated()
            if sprayState is False:
                sprayState = sprayActivated()

    # handling interrupt and system exit
    except (KeyboardInterrupt, SystemExit):
        print("Exiting sprayStepperMotor.py")
        GPIO.cleanup()


if __name__ == "__main__":
    main()

# FLAKE8 OUTPUT BELOW:
# spraySM.py:94:80: E501 line too long (80 > 79 characters)
# spraySM.py:96:80: E501 line too long (84 > 79 characters)
# spraySM.py:106:80: E501 line too long (87 > 79 characters)
# spraySM.py:134:80: E501 line too long (80 > 79 characters)
