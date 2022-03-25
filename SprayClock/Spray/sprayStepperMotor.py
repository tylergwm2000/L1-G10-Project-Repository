import pyrebase
from sense_hat import SenseHat
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

IN1= 7      # GPIO Control Output Pin // GPIO04 (1-wire)
IN2= 11     # GPIO Control Output Pin // GPIO17
IN3= 16     # GPIO Control Output Pin // GPIO24
IN4= 18     # GPIO Control Output Pin // GPIO23

control_pins = [IN1,IN2,IN3,IN4]

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
    [1, 0, 0, 1]
]

def moveSMon():
    print("spraying")
    for i in range(256):  # Stepper Motor to rotate COUNTERCLOCKWISE
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            sleep(0.001)

def moveSMoff():
    for i in range(256):  # Stepper Motor to rotate CLOCKWISE
        for halfstep in range(len(halfstep_seq)-1, -1, -1):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            sleep(0.001)

def initDatabase():

  config = {
    "apiKey": "AIzaSyDo00f19D_1SEPSYfjlNw9KkVkUNf-jyLw",
    "authDomain": "sprayclock-4e902.firebaseapp.com",
    "databaseURL": "https://sprayclock-4e902-default-rtdb.firebaseio.com/",
    "storageBucket": "sprayclock-4e902.appspot.com"
  }

  firebase = pyrebase.initialize_app(config)
  db = firebase.database()

  return db

def sprayActivated():

  print("sprayA")

  db = initDatabase()
  ds = "Subsystem Status"

  # checking the Alarm Clock Button value
  myAlarmClockButton = db.child(ds).child("Alarm Clock").child("Button").get()

  # checking the Alarm Clock Buzzer value
  myAlarmClockBuzzer = db.child(ds).child("Alarm Clock").child("Buzzer").get()
  # checking the Bed Detection Camera value
  myBedDetectionCamera = db.child(ds).child("Bed Detection").child("Camera").get()
  # checking the Bed Detection Load Sensor value
  myBedDetectionLoadSensor = db.child(ds).child("Bed Detection").child("Load Sensor").get()

  print("WOOT")

  # if the Alarm Clock Buzzer is currently ringing
  if myAlarmClockBuzzer.val() == True:
      # if there is someone that is sensed by the camera to be on the Bed Detection System
      if myBedDetectionCamera.val() == True:
          # if there is someone that is sensed by the load sensor to be on the Bed Detection System
          if myBedDetectionLoadSensor.val() == True:
              # then activate the Spray using the stepper motor
              db.child(ds).child("Spray").child("Stepper Motor").set(True) # DATA FORMAT True (Boolean)
              
              moveSMon()
              
              print("spray now activated")
              return True # The spray is activated
  print("spray still deactivated")
  return False # The spray is deactivated

def sprayDeactivated():

  print("sprayD")

  db = initDatabase()
  ds = "Subsystem Status"

  # checking the Alarm Clock Button value
  myAlarmClockButton = db.child(ds).child("Alarm Clock").child("Button").get()

  print(myAlarmClockButton)
  if myAlarmClockButton.val() == True:
      # then deactivate the Spray using the stepper motor
      db.child(ds).child("Spray").child("Stepper Motor").set(False) # DATA FORMAT False (Boolean)
      db.child(ds).child("Alarm Clock").child("Buzzer").set(False) # THIS IS NOT THE JOB OF THE SPRAY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      db.child(ds).child("Alarm Clock").child("Button").set(False) # THIS IS NOT THE JOB OF THE SPRAY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      
      moveSMoff()

      print("spray now deactivated")
      return False
  print("spray still activated")
  return True

def main():
    try:
        print("main")
        sprayState = sprayActivated()

        while True: # infinite loop, therefore, constantly checking
            if sprayState == True:
                sprayState = sprayDeactivated()
            if sprayState == False:
                sprayState = sprayActivated()

    except (KeyboardInterrupt, SystemExit): #Handling interrupt and system exit
        print("Exiting sprayStepperMotor.py")
        GPIO.cleanup()

if __name__ == "__main__":
  main()       
