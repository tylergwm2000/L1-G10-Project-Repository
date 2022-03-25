#spray.py implements the Spray Subsystem and uses the stepper motor.

import pyrebase
from sense_hat import SenseHat

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
      print("spray now deactivated")
      return False
  print("spray still activated")
  return True

def main():
  print("main")
  sprayState = sprayActivated()

  while True: # infinite loop, therefore, constantly checking
      if sprayState == True:
          sprayState = sprayDeactivated()
      if sprayState == False:
          sprayState = sprayActivated()

if __name__ == "__main__":
  main()
