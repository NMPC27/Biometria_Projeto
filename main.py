from threading import Thread
import customtkinter as Ctk
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os
import time

import numpy as np
import utils
import facedetection
import fingerprint
import requests
import json


endpoint = 'https://biometriapp.nunompcunha2001.workers.dev/'
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTkxMTAzMDAsImV4cCI6MTczMDY0NjMwMCwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.lRJ3CpOEdegZ4d45xTtUx3VvboPMcl4LQcvVv79IL0s"


#DEFINE 
X_POS=187
Y_POS=97
WIDTH=483
HEIGHT=393

MAX_X=155
MAX_Y=65
MAX_WIDTH=515
MAX_HEIGHT=425

MIN_X=220
MIN_Y=130
MIN_WIDTH=450
MIN_HEIGHT=360



Ctk.set_appearance_mode("Dark")   
Ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(Ctk.CTk):
    def __init__(self,vid):
        super().__init__()

        #video feed
        self.vid = vid
        #image currently in the video label
        self.img = None
        # configure window
        self.title("Biometria")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        self.frame = Ctk.CTkFrame(master=self,width=1100, height=580)
        self.frame.place(x=0, y=0)

        self.nfc()

    
    def PopUp(self,msg):
        """
        PopUp window with a message

        Args:
            msg (str): Message to display
        """
        pop_up= Ctk.CTkToplevel(self)
        pop_up.geometry("250x150+865+465")
        pop_up.title("Warning")
        Ctk.CTkLabel(pop_up, text= msg, font=('Arial',16)).place(x=125,y=75,anchor="center")


    
    def nfc(self, register=False):
        """
        NFC page, can be used for login or register, requires the user to use the NFC reader

        Args:
            register (bool, optional): If true, register a new user. Defaults to False.
        """
        self.user=None

        #clear frame
        for widget in self.frame.winfo_children():
            widget.destroy()


        #* Please use the NFC reader
        label = Ctk.CTkLabel(self.frame, text="Enter your NFC ID",font=("Arial", 20))
        label.place(x=480, y=40)
        
        nfcImg = Ctk.CTkImage(light_image=Image.open("./img/nfc.png"), size=(300 , 180))
        nfc_label = Ctk.CTkLabel(master=self.frame, image=nfcImg, text='')
        nfc_label.place(x=400, y=200)

        self.after(1000, self.getNfc) 

    def getNfc(self):
        res = requests.get(endpoint)
        tmp = json.loads(res.text)
        id = tmp["currentId"] 

        print(id)

        if id != "NULL":
            self.user = id

            if id in os.listdir("./db"): #login
                requests.post(endpoint, data=json.dumps({"token": TOKEN, "id": "NULL"})) 
                self.faceRecognition(register=False)
            else: #registar
                requests.post(endpoint, data=json.dumps({"token": TOKEN, "id": "NULL"})) 
                self.faceRecognition(register=True)

        else:
            self.after(1000, self.getNfc) 


    def faceRecognition(self, register=False):
        """
        Face recognition page, can be used for login or register, requires the user to use the camera

        Args:
            register (bool, optional): If true, register a new user. Defaults to False.
        """

        #clear frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        #frame for the video feed
        self.video_label = Ctk.CTkLabel(self.frame, fg_color="transparent", bg_color="transparent", text="")
        self.video_label.place(x=250, y=30)
        self.open_camera(register=register)
        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.nfc() )
        cancelBtn.place(x=410, y=540)

        self.nextBtn = Ctk.CTkButton(self.frame , text="Next")
        self.nextBtn.place(x=610, y=540)

        #start the face detection thread with arg register
        self.nextBtn.configure(command= lambda:Thread(target=self.face_detection, args=(register,)).start())

    def face_detection(self, register):
        """
        Verify user face
        """
        user=self.user
        #disable button
        self.nextBtn.configure(state="disabled")
        #start a timer
        start = time.time()
        blinks = 0
        last_blink = start
        last_image = self.img

        liveness = False
        while not liveness and time.time() - start < 10:
            #skip if no new image
            if self.img is last_image:
                continue

            blink_detected = facedetection.blink(self.img)
            #last blink was more than 0.5s ago
            if blink_detected and time.time() - last_blink > 0.5:
                blinks += 1
                last_blink = time.time()
            
            #if 2 blinks detected in 10s
            # print(blinks)
            if blinks >= 2:
                liveness = True

        if not liveness:
            self.PopUp("Liveness test failed")
            self.nextBtn.configure(state="normal")
            return
        else:
            #wait for image without eyes closed
            time.sleep(0.5)
            if register:
                success, error = facedetection.registerFace(self.img, user)
            else:
                success, error = facedetection.faceVerify(self.img, user)

            if success:
                self.fingerprint(register=register)
            else:
                self.PopUp(error)
                self.nextBtn.configure(state="normal")
                return


    def fingerprint(self, register=False):
        """
        Fingerprint page, can be used for login or register, requires the user to use the fingerprint reader

        Args:
            register (bool, optional): If true, register a new user. Defaults to False.
        """

        for widget in self.frame.winfo_children():
            widget.destroy()


        fingerImg = Ctk.CTkImage(light_image=Image.open("./img/finger.png"), size=(256 , 256))
        finger_label = Ctk.CTkLabel(master=self.frame, image=fingerImg, text='')
        finger_label.place(x=422, y=162)

        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.nfc())
        cancelBtn.place(x=410, y=540)

        nextBtn = Ctk.CTkButton(self.frame , text="Next", state="disabled")
        nextBtn.place(x=610, y=540)

        #*depois ver como se faz o loop para verificar se o sensor leu cenas
        #* funciona como teste, dá sempre 1, True
        if register:
            user, success = fingerprint.fingerprint_register()
            if success:
                self.user = user
                nextBtn.configure(state="normal")
                nextBtn.configure(command= lambda: self.registDone())
                
        else:
            user, success = fingerprint.fingerprint_login()
            if success:
                self.user = user
                nextBtn.configure(state="normal")
                nextBtn.configure(command= lambda: self.userPage())
            else:
                self.PopUp("Invalid fingerprint")


        #! TESTS ONLY
        nextBtn = Ctk.CTkButton(self.frame , text="TEST NEXT", command= lambda: self.userPage())
        nextBtn.place(x=610,  y=510)
        
        
    def registDone(self):
        """
        Registration done page
        """
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = Ctk.CTkLabel(self.frame, text="Regist Successful!", text_color="green",font=("Arial", 20))
        label.place(x=450, y=40)

        userImg = Ctk.CTkImage(light_image=Image.open("./img/register.png"), size=(256 , 256))
        user_label = Ctk.CTkLabel(master=self.frame, image=userImg, text='')
        user_label.place(x=422, y=162)

        doneBtn = Ctk.CTkButton(self.frame , text="Done", command= lambda: self.nfc() )
        doneBtn.place(x=480, y=540)

    def userPage(self):
        """
        User page, shows user ID
        """
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = Ctk.CTkLabel(self.frame, text="Authentication Successful!", text_color="green",font=("Arial", 20))
        label.place(x=450, y=40)

        userImg = Ctk.CTkImage(light_image=Image.open("./img/profile.png"), size=(256 , 256))
        user_label = Ctk.CTkLabel(master=self.frame, image=userImg, text='')
        user_label.place(x=422, y=162)

        doneBtn = Ctk.CTkButton(self.frame , text="Done", command= lambda: self.nfc() )
        doneBtn.place(x=480, y=540)
        self.open_camera()


    def open_camera(self, register = False):
        """
        gets camera frame and puts it on video label, draw green rectangle if registering a new user

        Args:
            register (bool, optional): If true, draw green rectangle. Defaults to False.
        """
        
        camera_frame = utils.capture_frame(vid,raw=True)
        #let this be acessible to other functions
        #!change brightness change second value
        # cv2.normalize(camera_frame, camera_frame, 0, 200, cv2.NORM_MINMAX)
        #!noise reduction
        camera_frame = cv2.GaussianBlur(camera_frame, (5, 5), 0)

        self.img = camera_frame

        image = camera_frame.copy()
        boxes = facedetection.detect_faces(image)
        
        for (x,y,w,h) in boxes:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)

        if register:
            cv2.rectangle(image,(X_POS,Y_POS),(WIDTH,HEIGHT),(0,255,0),3)


        image = utils.convert_to_photoimage(image)
  
        # put image in the label
        self.video_label.configure(image=image)
        #repeat every 15ms
        if register:
            self.video_label.after(15, self.open_camera, True)
        else:
            self.video_label.after(15, self.open_camera)



if __name__ == "__main__":
    vid = cv2.VideoCapture(0)
    #change exposure
    
    app = App(vid)

    pid = os.getpid()
    app.protocol("WM_DELETE_WINDOW", lambda: os.system(f"taskkill /pid {pid} /f"))

    app.mainloop()