#hx711.py implements code to function with HX711 breakout board that will be connected to the load sensor.
#Code will interact with HX711 board and load sensor for getting weight measurements.
#This code will be based off the following code found on the GitHub link:
#https://github.com/tatobari/hx711py

import RPi.GPIO as GPIO
from time import sleep


class HX711:
	#Initiate load sensor with BCM pins and gain(default 128)
	def __init__(self, dout, pd_sck, gain=128):
		self.GAIN = 0
		self.OFFSET = 0
		self.SCALE = 1
		GPIO.setmode(GPIO.BCM)
		self.PD_SCK = pd_sck
		self.DOUT = dout
		GPIO.setup(pd_sck, GPIO.OUT)
		GPIO.setup(dout, GPIO.IN)
		self.power_up()
		self.set_gain(gain)

	#Set gain of load sensor
	def set_gain(self, gain=128):
		try:
			if gain == 128:
				self.GAIN = 3
			elif gain == 64:
				self.GAIN = 2
			elif gain == 32:
				self.GAIN = 1
		except:
			self.GAIN = 3 #Default gain at 128

	#Set scale of load sensor
	def set_scale(self, scale):
		self.SCALE = scale

	#Set offset of load sensor
	def set_offset(self, offset):
		self.OFFSET = offset

	#Get the gain of load sensor
	def get_gain(self):
		if self.GAIN == 3:
			return 128
		elif self.GAIN == 2:
			return 64
		elif self.GAIN == 1:
			return 32

	#Get the scale of load sensor
	def get_scale(self):
		return self.SCALE

	#Get the offset of load sensor
	def get_offset(self):
		return self.OFFSET

	#Read data from HX711 chip, this code is based off of code in C programming language from document at following link:
	#https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf on page 8
	def read(self):
		#Check if chip is ready
		while (GPIO.input(self.DOUT) != 0):
			pass

		count = 0

		for i in range(24):
			GPIO.output(self.PD_SCK, True)
			count = count << 1
			GPIO.output(self.PD_SCK, False)
			if (GPIO.input(self.DOUT)):
				count += 1

		GPIO.output(self.PD_SCK, True)
		count = count ^ 0x800000
		GPIO.output(self.PD_SCK, False)
		#Set channel and gain factor for next reading
		for i in range(self.GAIN):
			GPIO.output(self.PD_SCK, True)
			GPIO.output(self.PD_SCK, False)

		return count

	#Get times readings from HX711 chip and return average value
	def read_average(self, times = 16):
		sum = 0
		for i in range(times):
			sum += self.read()
		return sum / times

	#Get average value and convert it to grams
	def get_grams(self, times = 16):
		value = (self.read_average(times) - self.OFFSET)
		grams = (value/self.SCALE)
		return grams

	#Zero functionality for calibration
	def tare(self, times = 16):
		sum = self.read_average(times)
		self.set_offset(sum)

	#Power the HX711 chip down
	def power_down(self):
		GPIO.output(self.PD_SCK, False)
		GPIO.output(self.PD_SCK, True)

	#Power the HX711 chip up
	def power_up(self):
		GPIO.output(self.PD_SCK, False)
