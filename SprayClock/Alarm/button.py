import RPi.GPIO as GPIO

def buttonPressed(channel):
        print("Buttonpressed")
GPIO.setwarnings(False) # No warning will be recognized at the time
GPIO.setmode(GPIO.BCM) # This will be used to let us use pin numbers
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin
GPIO.add_event_detect(14,GPIO.RISING,callback=buttonPressed) # Adding an event from pin 14
statement = input("If you want to quit, press enter\n\n") # Program will run until someone has clicked enter
GPIO.cleanup()
