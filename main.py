#modules used
import face_recognition 
import cv2
import numpy as np
import csv
import os
from playsound import playsound
from datetime import datetime
import pandas as pd
from subprocess import call

#laptop camera
video_capture=cv2.VideoCapture(0)

#path where the images of students are stored
path = 'C:/Users/LENOVO/Desktop/Secound screen/Minor Project/images'
images =[]
myList = os.listdir(path)
known_faces_encodings=[]
known_faces_names=[]
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    known_faces_names.append(os.path.splitext(cl)[0])
    print(known_faces_names)

#Encoding the faces
def findEncodings(images):
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        known_faces_encodings.append(encode)
    return known_faces_encodings

student=known_faces_names.copy()

face_loc=[]
face_encodings=[]
face_name=[]
s=True

nowdate = datetime.now()
current_date=nowdate.strftime("%d-%m-%Y")

#creating csv file
f = open(current_date+".csv","w+",newline='')
lnwriter=csv.writer(f)
lnwriter.writerow(["Name","Roll no","Time"])

known_faces_encodings = findEncodings(images)
#will print this after the encoding of the faces are completed
print('Encoding Complete')
#this will look at the camera feed for and find the best matches of faces from the stored student images
while True:
    ret, frame=video_capture.read()
    small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    small_frame=cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    if s:
        face_locations= face_recognition.face_locations(small_frame)
        face_encodings=face_recognition.face_encodings(small_frame, face_locations)
        face_names=[]
        for face_encoding in face_encodings:
            matches=face_recognition.compare_faces(known_faces_encodings, face_encoding)
            name=""
            face_distance=face_recognition.face_distance(known_faces_encodings,face_encoding)
            best_match_index= np.argmin(face_distance)
            if matches[best_match_index]:
                name= known_faces_names[best_match_index]
            face_names.append(name)
            if name in known_faces_names:
                if name in student:
                    roll_no=known_faces_names.index(name)+1
                    student.remove(name)
                    print(student)
                    nowtime = datetime.now()
                    current_time = nowtime.strftime("%H:%M:%S")
                    playsound("attendance.wav")
                    lnwriter.writerow([name.capitalize(),roll_no,current_time])
            

    cv2.imshow("attendence sys",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
#executing the webapp.py file
call(["python", "webapp.py"])