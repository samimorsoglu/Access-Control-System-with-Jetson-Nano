import time
import datetime
from datetime import date
from time import sleep
import sys
from Jetson_MFRC522 import SimpleMFRC522
import mysql.connector 
from mysql.connector import connection
import Jetson.GPIO as GPIO
from imutils.video import VideoStream
from imutils.video import FPS
from gtts import gTTS
from playsound import playsound
import face_recognition
import imutils
import pickle
import time
import cv2

GPIO.setwarnings(False)

j=0
count = 0
led_pin = 12
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 

while True:

	db1 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db2 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db3 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db4 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db5 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db6 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db7 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db9 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db10 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	db11 = mysql.connector.connect(
	  host="localhost",
	  user="admin",
	  passwd="matrak123",
	  database="project3"
	)
	a=0
	cursor_student = db2.cursor()
	cursor_instructor = db1.cursor()
	cursor_attendance = db3.cursor()
	cursor_admin_id = db4.cursor()
	cursor_student_id = db5.cursor()
	cursor_attendance_id=db6.cursor()
	cursor_final=db7.cursor()
	cursor_student_empty=db9.cursor()
	cursor_enrollment_max=db10.cursor()
	cursor_get_student=db11.cursor()
	reader = SimpleMFRC522()

	print('\nYoklamayı Baslatmak Icin Yetkili Kartını Okutunuz\n')
	id, text = reader.read()		
	cursor_instructor.execute("Select id, name FROM student_management_app_instructor WHERE rfid_uid="+str(id))	
	result = cursor_instructor.fetchone()
	if cursor_instructor.rowcount >= 1:
		print("Yetkili Girisi Basarılı \nHosgeldiniz Sayın " + text)
		mytext=("Hoşgeldiniz Sayın "+text)
		myOutput=gTTS(text=mytext, lang='tr', slow=False)
		myOutput.save('talk.mp3')
		playsound('/home/altan/Desktop/facial_recognition/talk.mp3')
		a=a+1
		now = datetime.datetime.now()

		insert_query2 = """INSERT INTO student_management_app_attendance (course_id_id,attendance_date) VALUES (%s,%s)"""
		cursor_attendance.execute(insert_query2, (result[0],now.strftime('%Y-%m-%d %H:%M:%S')))
		db3.commit()

		cursor_attendance_id.execute("Select id FROM student_management_app_attendance ORDER BY attendance_date DESC LIMIT 1")	
		attendance_id = cursor_attendance_id.fetchone()
		
		student_ids = []
		cursor_get_student.execute("Select student_id_id FROM student_management_app_enrollment WHERE course_id_id="+str(result[0]))	
		student_id = cursor_get_student.fetchall() 
		student_ids = list(student_id)
		

		for student in student_ids:
			insert_query4 = """INSERT INTO student_management_app_attendancereport (status,attendance_id_id,student_id_id) VALUES (%s,%s,%s)"""
			cursor_student_empty.execute(insert_query4, (0,attendance_id[0],student[0]))
			db9.commit()
	else:
		print("Yoklama Sistemi Aktif Değil\nLutfen Yetkilinin Yoklamayi Acmasini Bekleyin\n")
		mytext5=("Yoklama aktif değil.Lütfen yetkilinin yoklamayı açmasını bekleyin")
		myOutput=gTTS(text=mytext5, lang='tr', slow=False)
		myOutput.save('talk.mp3')
		playsound('/home/altan/Desktop/facial_recognition/talk.mp3')		
	time.sleep(2)


	try:
		while a%2 == 1:

				print('\nLutfen Ogrenci Kartınızı Okutunuz\n')
				id, text = reader.read()
				
				cursor_student.execute("Select id, first_name FROM student_management_app_customuser WHERE card_uid="+str(id))
				result = cursor_student.fetchone()
				
				if cursor_student.rowcount >= 1:
					GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 
					GPIO.output(led_pin, GPIO.HIGH)
					vs = VideoStream(src=0,framerate=10).start()
					currentname = "unknown"
					encodingsP = "encodings.pickle"
					print("Yuz Tanıma Islemi Baslatıldı\nLutfen Kameraya Bakınız\n")
					mytext3=("Yüz Tanıma İşlemi Başlatıldı.Lütfen Kameraya Bakınız")
					myOutput=gTTS(text=mytext3, lang='tr', slow=False)
					myOutput.save('talk.mp3')
					playsound('/home/altan/Desktop/facial_recognition/talk.mp3')
					data = pickle.loads(open(encodingsP, "rb").read())

					

					while True:
						
						frame = vs.read()
						frame = imutils.resize(frame, width=300)
						
						boxes = face_recognition.face_locations(frame)
						
						encodings = face_recognition.face_encodings(frame, boxes)
						names = []

						
						for encoding in encodings:
							
							matches = face_recognition.compare_faces(data["encodings"],
								encoding)
							name = "Unknown" 

							
							if True in matches:
								
								matchedIdxs = [i for (i, b) in enumerate(matches) if b]
								counts = {}

								
								for i in matchedIdxs:
									name = data["names"][i]
									counts[name] = counts.get(name, 0) + 1

							
								name = max(counts, key=counts.get)

								
								if currentname != name:
									currentname = name
									
									if text[0:11] == currentname[0:11]:
										insert_query = """INSERT INTO student_management_app_face (student_num) VALUES (%s)"""
										cursor_student.execute(insert_query, (currentname,))
										db2.commit()

										cursor_admin_id.execute("Select id FROM student_management_app_customuser WHERE student_num="+str(currentname))	
										admin_id = cursor_admin_id.fetchone()
		
										cursor_student_id.execute("Select id FROM student_management_app_students WHERE admin_id="+str(admin_id[0]))	
										student_id = cursor_student_id.fetchone()
										insert_query3 = """UPDATE student_management_app_attendancereport SET status = %s WHERE student_id_id = %s AND attendance_id_id = %s"""
										cursor_final.execute(insert_query3, (1,student_id[0], attendance_id[0]))
										db7.commit()
										GPIO.output(led_pin, GPIO.LOW)

										print("Hosgeldiniz " + currentname )
										print("\nYoklama Kaydınız Alınmıstır\nIyi Dersler :)\n")
										mytext4=("İyi Dersler")
										myOutput=gTTS(text=mytext4, lang='tr', slow=False)
										myOutput.save('talk.mp3')
										playsound('/home/altan/Desktop/facial_recognition/talk.mp3')	
									elif text != currentname:
										GPIO.output(led_pin, GPIO.LOW)
										print("Lutfen Sadece Kendi Kartınızı Kullanınız")
										time.sleep(2)
									else:	
										GPIO.output(led_pin, GPIO.LOW)
										print("Sistemde Bir Sorun var,Lutfen Yetkili Ile Iletisime Gecin")

							
							names.append(name)
						
						for ((top, right, bottom, left), name) in zip(boxes, names):
							
							cv2.rectangle(frame, (left, top), (right, bottom),
								(0, 255, 225), 2)
							y = top - 15 if top - 15 > 15 else top + 15
							cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
								.8, (0, 255, 255), 2)

						cv2.imshow("Yuz Tanima Ani", frame)
						key = cv2.waitKey(1) & 0xFF

					
						if currentname != "unknown":
							time.sleep(4)
							cv2.destroyAllWindows()
							vs.stream.release()
							break

						
				
				else:
					id, text = reader.read()		
					cursor_instructor.execute("Select id, name FROM student_management_app_instructor WHERE rfid_uid="+str(id))		
					result = cursor_instructor.fetchone()
					if cursor_instructor.rowcount >= 1:
						a=a+1
						print("Yoklama Basarı Ile Alındı. \nIyı Dersler Sayın " + text)
						mytext2=("Yoklama Başarı İle Alındı.İyi Dersler Sayın " + text)
						myOutput=gTTS(text=mytext2, lang='tr', slow=False)
						myOutput.save('talk.mp3')
						playsound('/home/altan/Desktop/facial_recognition/talk.mp3')	
						time.sleep(2)
					else:			
						print("Derse Kaydınız Bulunmamaktadır \nLutfen Yetkili Ile Iletisime Gecin")
						mytext4=("Derse Kaydınız Bulunmamaktadır.Lütfen Yetkili ile iletişime geçin")
						myOutput=gTTS(text=mytext4, lang='tr', slow=False)
						myOutput.save('talk.mp3')
						playsound('/home/altan/Desktop/facial_recognition/talk.mp3')
						time.sleep(2)
		

	finally:
			GPIO.cleanup()
