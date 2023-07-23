import cv2
import numpy as np
from imutils import face_utils
from preferredsoundplayer import playsound
from threading import Thread
import datetime
from tkinter import *
import PIL.Image , PIL.ImageTk
import time

class Functions():
    def __init__(self):
        #Status marking for current state
        self.sleep  = 0
        self.drowsy = 0
        self.active = 0
        self.status = ""
        self.color  = None
        self.check  = None
        self.audio  = r"/home/pi/Documents/Drowsy/Audio/Wakeup.mp3"
        self.audio_no_face = r"/home/pi/Documents/Drowsy/Audio/no_face.mp3"
        self.last_alert = None
        self.alert_each = 10
        self.RCVPhoto = None
        self.LCVPhoto = None
        self.start_time = None
        self.no_face_duration = 0
        self.pre_condition = False

    def compute(self,ptA,ptB):
        return np.linalg.norm(ptA - ptB)
    
    def blinked(self,a,b,c,d,e,f):
        up = self.compute(b,d) + self.compute(c,e)
        down = self.compute(a,f)
        ratio = up/(2.0*down)
        #Checking if it is blicked
        if (ratio > 0.25):
            return 2
        elif (ratio > 0.21 and ratio <= 0.25):
            return 1
        else:
            return 0

    def subalert(self):
        playsound(self.audio)

    def no_Face_Alert(self):
        playsound(self.audio_no_face)
        
    def alert(self,frame,speed):
        if (self.check == 0):
            self.status = "SLEEPING !!!"
            self.color = (0,0,255)
            if (self.last_alert is None) or ((datetime.datetime.utcnow() - self.last_alert).total_seconds() > self.alert_each):
                self.last_alert = datetime.datetime.utcnow()
                if (speed == 1):
                    t1 = Thread(target=self.subalert) 
                    t1.start()
        elif (self.check == 1):
            self.status = "DROWSY !!"
            self.color = (255,0,0)
        else :
            self.status="ACTIVE"
            self.color = (0,255,0)
            self.pre_condition = True
        cv2.putText(frame,self.status,(0,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,self.color,2)

    def calculate(self,frame,face_detect,landmark_detect,face_frame,RCV,LCV,speed):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detect(gray)
        if (self.pre_condition == True):
            if len(faces) > 0:
                self.start_time = None
                self.no_face_duration = 0
            elif self.start_time is None:
                self.start_time = time.time()
            else:
                self.no_face_duration = time.time() - self.start_time
            if self.no_face_duration >= 5 and speed == 1:
                if (self.last_alert is None) or ((datetime.datetime.utcnow() - self.last_alert).total_seconds() > self.alert_each):
                    self.last_alert = datetime.datetime.utcnow()
                    t1 = Thread(target=self.no_Face_Alert) 
                    t1.start()
                
        
        #Detected face in faces array
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            face_frame = frame.copy()
            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            landmarks = landmark_detect(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)
            #The numbers are actually the landmarks which will show eye
            left_blink = self.blinked(landmarks[36],landmarks[37], 
                landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = self.blinked(landmarks[42],landmarks[43], 
                landmarks[44], landmarks[47], landmarks[46], landmarks[45])
            
            if(left_blink== 0 or right_blink==0):
                self.sleep+=1
                self.drowsy=0
                self.active=0
                if(self.sleep>10):
                    self.check = 0
            elif(left_blink==1 or right_blink==1):
                self.sleep=0
                self.active=0
                self.drowsy+=1
                if(self.drowsy>6):
                    self.check = 1
            else:
                self.drowsy=0
                self.sleep=0
                self.active+=1
                if(self.active>6):
                    self.check = 2
            self.alert(frame,speed)

            for n in range(0,68):
                (x,y) = landmarks[n]
                cv2.circle(face_frame,(x,y),1,(255,255,255),-1)
        #Opencv is BGR but tkinter is RGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        face_frame = cv2.cvtColor(face_frame,cv2.COLOR_BGR2RGB)
        #Bỏ khung hình vô trong photo ,conver ảnh đọc được thành image thì mới hiển thị được
        self.RCVPhoto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.LCVPhoto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(face_frame))
        #Show
        RCV.create_image(0,0,image = self.RCVPhoto,anchor=NW)
        LCV.create_image(0,0,image = self.LCVPhoto,anchor=NW)

        return self.check
