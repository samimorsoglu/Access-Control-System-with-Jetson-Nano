from time import sleep
import sys
from Jetson_MFRC522 import SimpleMFRC522
import os 
from gtts import gTTS
from playsound import playsound
reader = SimpleMFRC522()


while True:
		
	print("Hold a tag near the reader")
	id, text = reader.read()
	print("ID: %s\nText: %s" % (id,text))
	mytext=("Hoşgeldiniz"+text)
	myOutput=gTTS(text=mytext, lang='tr', slow=False)
	myOutput.save('talk.mp3')
	playsound('/home/altan/Desktop/facial_recognition/talk.mp3')
	sleep(5)

