#camera.py uses TensorFlow Lite object detection model to perform object detection on an image it receives from bedDetection.py.
#This code is based off the TensorFlow Lite label_image.py code on GitHub at the following link:
#https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py

import argparse
from time import sleep
import numpy as np
from PIL import Image
import sys
import cv2
import os
from picamera import PiCamera
from tflite_runtime.interpreter import Interpreter

class Camera:
	def init_camera():
		camera = PiCamera()
		camera.resolution = (1920, 1080)
		#camera.sensor_mode = 3
		#camera.iso = 0
		#camera.framerate = 0.167
		#camera.exposure_mode = 'nightpreview'
		return camera

	def take_image(camera, imagefile):
		camera.capture(imagefile)

	def camera_detection(image, model, label):
		personDetected = False #Initial boolean variable
		min_confidence_threshold = 0.5 #Minimum confidence to pass
		graph_name = 'detect.tflite' #Name of tflite file
		labelmap_name = 'labelmap.txt' #Name of labelmap file
		current_dir = os.getcwd() #Current directory

		#Paths to image, model, and label
		path_to_image = os.path.join(current_dir, image)
		path_to_model = os.path.join(current_dir, model)
		path_to_label = os.path.join(current_dir, label)

		#Load label map into list and remove weird first label of ???
		with open(path_to_label, 'r') as f:
			labels = [line.strip() for line in f.readlines()]
		del(labels[0])

		#Load Tensorflow Lite model
		interpreter = Interpreter(model_path = path_to_model)
		interpreter.allocate_tensors()

		#Get model details
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()
		height = input_details[0]['shape'][1]
		width = input_details[0]['shape'][2]
		floating_model = (input_details[0]['dtype'] == np.float32)

		#Check if model is created for TensorFlow2 or TensorFlow1
		outname = output_details[0]['name']
		if ('StatefulPartitionedCall' in outname): #TensorFlow2 model
			boxes_idx = 1
			classes_idx = 3
			scores_idx = 0
		else: #TensorFlow1 model
			boxes_idx = 0
			classes_idx = 1
			scores_idx = 2

		#Load image and resize to expected shape
		image = cv2.imread(path_to_image) #read image
		image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #change image to rgb
		image_resized = cv2.resize(image_rgb, (width, height)) #resize rgb image
		inputdata = np.expand_dims(image_resized, axis = 0) #Expand shape of array
		if floating_model: #Normalize pixel values if using floating model(Non-quantized model)
			inputdata = (np.float32(inputdata) - 127.5)/127.5

		#Perform object detection by running model with image as input
		interpreter.set_tensor(input_details[0]['index'], inputdata)
		interpreter.invoke()
		classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] #Class index of detected objects
		scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] #Confidence of detected objects
		#Loop through all detected objects
		for i in range(len(scores)):
			object = labels[int(classes[i])] # Get object name from labels list using class index
			print('{} detected with {}% confidence'.format(object, int(scores[i]*100)))
			if ((scores[i] > min_confidence_threshold) and (scores[i] <= 1.0)):
				if (object == 'person'):
					personDetected = True
		return personDetected
