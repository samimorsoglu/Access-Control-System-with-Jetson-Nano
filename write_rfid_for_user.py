from time import sleep
import sys
from Jetson_MFRC522 import SimpleMFRC522
reader = SimpleMFRC522()



try:
    while True:
 
            text = input('New data:')
            print("Now place your tag to write")
            reader.write(text)
            print("Written")
            print()

except KeyboardInterrupt:
    GPIO.cleanup()
    raise
