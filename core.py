#######################
"""
Import Packages -> Core.py
"""
#######################

# Import Modules
import json
import playsound
from datetime import date
import os
import speech_recognition as sr
import random

# Import Speech Synthesizing Modules
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# Define A Path for Json File Containing DB Data for User
path = './user.json'

# existence(variable -> checking for existence of path)
existence = os.path.exists(path)

# while existence
if existence:
	# open(variable -> opening the file)
	opened = open('user.json')
	
	# data(variable -> reading the file)
	data = json.load(opened)
	
	# close opened
	opened.close()

	# cd main/python main.py (redirect to main)
	os.chdir("main")
	os.system("python main.py")

# if not existence(new user)
else:
	# Define Variable for Speech Synthesis
	apikey = '3k6i8lvhuVL0xvMjdc3H0Fe5wciOJ-qN--UhqVPQNsev'
	url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/c0e720ca-1373-4cbb-959f-bae7d48795e0'

	# Authenticate
	authenticator = IAMAuthenticator(apikey)
	tts = TextToSpeechV1(authenticator=authenticator)
	tts.set_service_url(url)
	
	# Open mp3 file
	filename  = 'speech' + str(random.randint(1,100)) + '.mp3'
	with open(filename, 'wb') as audio_file:

		#  Synthesize
		res = tts.synthesize("A new user I see. Welcome. Welcome to Seven. Let me introduce myself. I'm Seven. I'm a damn brilliant guy. That's all. Here let me get you through setup. Spell your name.", accept='audio/mp3',
							 voice='en-US_KevinV3Voice').get_result()
		audio_file.write(res.content)

	# Play File
	try:
		playsound.playsound(filename)
		os.remove(filename)
		continueInput = True
	
	except:
		os.remove(filename)
		playsound.playsound(filename)
		continueInput = True

	while continueInput:
		# use the microphone as source for input.
		with sr.Microphone() as source:

			# Define the Recognizer
			r = sr.Recognizer()

			# the surrounding noise level
			r.adjust_for_ambient_noise(source, duration=0.2)
			
			# Use Pause Threshold
			r.pause_threshold = 1
			
			print("Listening....")

			audio = r.listen(source)

			# Using google to recognize audio
			inputtext = r.recognize_google(audio)
			
			# Lower input text
			inputtext = inputtext.lower()
			
			# Replace empty spaces
			inputtext = inputtext.replace(" ", "")
			if inputtext:
				with open(filename, 'wb') as audio_file:
					res = tts.synthesize(f"Is {inputtext} your name? If Yes(Press y), If No(Press n)", accept='audio/mp3',
										voice='en-US_KevinV3Voice').get_result()
					audio_file.write(res.content)
				
				playsound.playsound(filename)
				os.remove(filename)

				checkTrue = input("Is your name {0}? (y/n)".format(inputtext))
				if checkTrue == "y":
					dateCreated = str(date.today().day) + "/" + \
										str(date.today().month) + \
										"/" + str(date.today().year)
					jsonData = {"name": inputtext, "dateCreated": dateCreated}

					# Dump Data
					jsonString = json.dumps(jsonData)

					# Open Json File
					jsonFile = open("user.json", "w")

					# Write data
					jsonFile.write(jsonString)
					jsonFile.close()
				
				else:
					os.system("py core.py")
			
			# Define variables for user.json
			dateCreated = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
			jsonData = {"name": inputtext, "dateCreated": dateCreated}
			
			# Dump Data
			jsonString = json.dumps(jsonData)
			
			# Open Json File
			jsonFile = open("user.json", "w")
			
			# Write data
			jsonFile.write(jsonString)
			jsonFile.close()

		# Begin the app for marketing/explaining purposes
		os.chdir("app")
		os.system("npm start")



