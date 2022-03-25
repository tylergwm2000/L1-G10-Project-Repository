import sprayStepperMotor
import pytest
from time import sleep

db = sprayStepperMotor.initDatabase()

#Test if one can turn ON spray through STEPPER MOTOR by updating firebase values
# Getting and checking values work in the case
def test_turnOnSM():
    db.child("Subsystem Status").child("Bed Detection").child("Camera").set(True) #Update value for Camera from Firebase
    db.child("Subsystem Status").child("Bed Detection").child("Load Sensor").set(True) #Update value for Load Sensor from Firebase
    db.child("Subsystem Status").child("Alarm Clock").child("Buzzer").set(True) #Update value for Buzzer from Firebase
    db.child("Subsystem Status").child("Alarm Clock").child("Button").set(False) #Update value for Button from Firebase

    actualVal = sprayStepperMotor.sprayActivated() #Check if value from Firebase is same as sprayDeactivated method value returned
    print(actualVal)

    dataSM = db.child("Subsystem Status").child("Spray").child("Stepper Motor").get() #Get value for Stepper Motor from Firebase

    assert dataSM.val() == actualVal #Check if value from Firebase is same as sprayDeactivated method value returned

#Test if one can turn OFF spray through STEPPER MOTOR by updating firebase values
# Getting and checking values work in the case
def test_turnOffSM():
    db.child("Subsystem Status").child("Alarm Clock").child("Buzzer").set(False) #Update value for Buzzer from Firebase
    db.child("Subsystem Status").child("Alarm Clock").child("Button").set(True) #Update value for Button from Firebase

    actualVal = sprayStepperMotor.sprayDeactivated() #Check if value from Firebase is same as sprayDeactivated method value returned
    print(actualVal)

    dataSM = db.child("Subsystem Status").child("Spray").child("Stepper Motor").get() #Get value for Stepper Motor from Firebase

    assert dataSM.val() == actualVal #Check if value from Firebase is same as sprayDeactivated method value returned

#Test if case in between BUTTON ON and BUZZER ON works to turn OFF STEPPER MOTOR by updating firebase values works
#def test_betweenSwitchingSM() and ensure rotation of Stepper Motor is occurring:

def test_rotateStepperMotor():
    sprayStepperMotor.moveSMon()
    #Visually ensure the Stepper Motor has rotated 180 degrees counterclockwise
    #(512 steps equals full rotation, therefore, rotating 256 steps)

    sleep(5)

    sprayStepperMotor.moveSMoff()
