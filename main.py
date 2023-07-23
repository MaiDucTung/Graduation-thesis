import dlib
from imutils.video import VideoStream
from sub import Functions
from tkinter import *
from PIL import ImageTk, Image
import os
import time
from threading import Thread,Event
from preferredsoundplayer import playsound
import serial



def shutdown():
    os.system("sudo shutdown -h now")

def status_active():
    label_status.config(image=img_active)
def status_drowsy():
    label_status.config(image=img_drowsy)
def status_sleep():
    label_status.config(image=img_sleep)

def update_frame():
    global RCV ,LCV ,speed
    if (ser.in_waiting>0):
        speed = int(ser.readline().decode())
    frame = video.read()
    face_frame = video.read()
    check = method.calculate(frame,face_detect,landmark_detect,face_frame,RCV,LCV,speed)
    if (check == 2):
        status_active()
    elif (check == 1):
        status_drowsy()
    elif (check == 0):
        status_sleep()
    window.after(15 ,update_frame)

def timer(hours,countdown_label):
    seconds = hours * 3600
    start_time = time.time()
   
    while  not stop_event.is_set():
        # if (speed == 1):
        elapsed_time = int(time.time() - start_time)
        hours_elapsed = elapsed_time // 3600
        minutes_elapsed = (elapsed_time % 3600) // 60
        seconds_elapsed = (elapsed_time % 3600) % 60
        time_str = f"{hours_elapsed:02d}:{minutes_elapsed:02d}:{seconds_elapsed:02d}"
        countdown_label.config(text=time_str)
        time.sleep(1)
        if elapsed_time >= seconds:
            break
    countdown_label.config(text="Time's up!")
    playsound(r"/home/pi/Documents/Drowsy/Audio/time_4.mp3")
    if stop_event.is_set():
        countdown_label.config(text="Timer stopped!")

def on_close():
    global stop_event
    stop_event.set()
    window.destroy()

if __name__ == '__main__':
    speed = 0 
    #***********************CAN***********************
    ser = serial.Serial('/dev/ttyACM0',115200, timeout=1.0)
    time.sleep(3)
    ser.reset_input_buffer()
    #========================= Load Method =========================
    method = Functions()
    #========================= Interface =========================
    window = Tk()
    window.title("Sleep Detection Program")
    #========================= Background =========================
    background_path = Image.open(r"/home/pi/Documents/Drowsy/Photo/BSC37.jpeg")
    background= ImageTk.PhotoImage(background_path)
    window.geometry('1080x1920')
    label1 = Label(window,image=background)
    label1.place(x=0,y=0)
    #========================= Button =========================
    img_button = Image.open(r"/home/pi/Documents/Drowsy/Photo/button1.png")
    img_button = ImageTk.PhotoImage(img_button)
    button = Button(label1,image=img_button,command=shutdown)
    button.place(x=500,y=1600)
    #========================= Status =========================
    img_active = ImageTk.PhotoImage(Image.open(r"/home/pi/Documents/Drowsy/Photo/Active.png"))
    img_drowsy = ImageTk.PhotoImage(Image.open(r"/home/pi/Documents/Drowsy/Photo/Drowsy.png"))
    img_sleep = ImageTk.PhotoImage(Image.open(r"/home/pi/Documents/Drowsy/Photo/Sleep.png"))
    img_none = ImageTk.PhotoImage(Image.open(r"/home/pi/Documents/Drowsy/Photo/None.png"))
    label_status = Label(window,image=img_none)
    label_status.place(x=110,y=1325)
    #========================= Canvas =========================
    RCV = Canvas(window,width=450,height=450)
    RCV.place(relx=0.57, rely=0.5, anchor=W)
    LCV = Canvas(window,width=450,height=450)
    LCV.place(relx=0.43, rely=0.5, anchor=E)

    countdown_label = Label(window,text='',font=("Arial",50),fg="white",background="black")
    countdown_label.place(x=700,y=1350)
    #Initializing the face detector and landmark detector
    face_detect = dlib.get_frontal_face_detector()
    landmark_detect = dlib.shape_predictor(r"/home/pi/Documents/Drowsy/Models/shape_predictor_68_face_landmarks.dat")
    #Initializing the camera and taking the instance
    video = VideoStream(src=0).start()
    #========================= Countdown =========================
    stop_event = Event()
    window.protocol("WM_DELETE_WINDOW",on_close)
    time_thread = Thread(target=timer , args=(4,countdown_label))
    time_thread.start()

    update_frame()
    window.mainloop()