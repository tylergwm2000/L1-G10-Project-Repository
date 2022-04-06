import pyrebase
from time import sleep
import RPi.GPIO as GPIO

#GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#ULN2003 Setup
IN1= 7      # GPIO Control Output Pin // GPIO04 (1-wire)
IN2= 11     # GPIO Control Output Pin // GPIO17
IN3= 16     # GPIO Control Output Pin // GPIO24
IN4= 18     # GPIO Control Output Pin // GPIO23

control_pins = [IN1,IN2,IN3,IN4]

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

# 2D array sequence of data values to rotate stepper motor counter clockwise
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

def moveSMCCW(steps):
    print("Rotating counter clockwise")
    rotations = steps * 256
    for i in range(rotations):  # Stepper Motor to rotate COUNTERCLOCKWISE for steps number of rotations
        for halfstep in range(8): # Starting sequence at top of 2D array
            for pin in range(4): # Send a sequence of data values to stepper motor driver board every 0.001 seconds
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            sleep(0.001)

def moveSMCW(steps):
    print("Rotating clockwise")
    rotations = steps * 256
    for i in range(rotations):  # Stepper Motor to rotate CLOCKWISE for steps number of rotations
        for halfstep in range(len(halfstep_seq)-1, -1, -1): # Starting sequence at bottom of 2D array
            for pin in range(4): # Sennd a sequence of data values to stepper motor driver board every 0.001 seconds
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

def sprayActivated(ringingLength):

  #print("sprayA")

  db = initDatabase()
  ds = "Subsystem Status"

  # checking the Alarm Clock Button value
  myAlarmClockButton = db.child(ds).child("Alarm Clock").child("Button").get().val()

  # checking the Alarm Clock Buzzer value
  myAlarmClockBuzzer = db.child(ds).child("Alarm Clock").child("Buzzer").get().val()
  # checking the Bed Detection Camera value
  myBedDetectionCamera = db.child(ds).child("Bed Detection").child("Camera").get().val()
  # checking the Bed Detection Load Sensor value
  myBedDetectionLoadSensor = db.child(ds).child("Bed Detection").child("Load Sensor").get().val()

  #print("WOOT")

  # if the Alarm Clock Buzzer is currently ringing, and someone is sensed by camera and load sensor in Bed Detection Subsystem
  if myAlarmClockBuzzer and myBedDetectionCamera and myBedDetectionLoadSensor:
      # then activate the Spray using the stepper motor if alarm has been ringing for 5 minutes
      if ringingLength >= 5:
          db.child(ds).child("Spray").child("Stepper Motor").set(True) # DATA FORMAT True (Boolean)
          # move stepper motor 3 rotations counter clockwise then 3 rotations clockwise
          moveSMCCW(3) #spray bottle pressed state
          sleep(1)
          moveSMCW(3) #spray bottle unpressed state
          print("spray now activated")
          return True # The spray is activated
  print("spray still deactivated")
  return False # The spray is deactivated

def sprayDeactivated():

  #print("sprayD")

  db = initDatabase()
  ds = "Subsystem Status"

  # checking the Alarm Clock Button value
  myAlarmClockButton = db.child(ds).child("Alarm Clock").child("Button").get().val()

  #print(myAlarmClockButton)
  if myAlarmClockButton:
      # then deactivate the Spray using the stepper motor
      db.child(ds).child("Spray").child("Stepper Motor").set(False) # DATA FORMAT False (Boolean)
      #These 2 lines of code should not be here delete them
      #db.child(ds).child("Alarm Clock").child("Buzzer").set(False) # THIS IS NOT THE JOB OF THE SPRAY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      #db.child(ds).child("Alarm Clock").child("Button").set(False) # THIS IS NOT THE JOB OF THE SPRAY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      
      #Move stepper motor 5 rotations clockwise (spray bottle unpressed state)
      moveSMCW(5)

      print("spray now deactivated")
      return False
  print("spray still activated")
  return True

def main():
    try:
        #print("main")
	db = initDatabase()
	timelength = 0 # Represents number of minutes alarm has been ringing for
        sprayState = sprayActivated()
        while True: # infinite loop, therefore, constantly checking
	    alarmRinging = db.child("Subsystem Status").child("Alarm Clock").child("Buzzer").get().val()
            if sprayState == True: # Check for deactivation condition
                sprayState = sprayDeactivated()
            if sprayState == False: # Check for activation condition
                sprayState = sprayActivated(timelength)
	    if alarmRinging: # Increase timelength for every minute alarm rings
                timelength = timelength + 1
            sleep(60)

    except (KeyboardInterrupt, SystemExit): #Handling interrupt and system exit
        print("Exiting sprayStepperMotor.py")
        GPIO.cleanup()

if __name__ == "__main__":
  main()       
