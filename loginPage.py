import customtkinter as Ctk
import cv2
import face_detection
from PIL import Image, ImageTk
from deepface import DeepFace
import threading

from faceVerifyPage import *

def login(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    allowNext = "disabled"

    nfcImg = Ctk.CTkImage(light_image=Image.open("./nfc.png"), size=(300 , 180))
    nfc_label = Ctk.CTkLabel(master=frame, image=nfcImg, text='')
    nfc_label.place(x=400, y=200)


    cancelBtn = Ctk.CTkButton(frame , text="Cancel", command=lambda: print("not implemented"))
    cancelBtn.place(x=410,  y=540)
    nextBtn = Ctk.CTkButton(frame , text="Next", state=allowNext, command= lambda: faceVerify(frame))
    nextBtn.place(x=610,  y=540)

    #! TESTS ONLY
    nextBtn = Ctk.CTkButton(frame , text="TEST NEXT", command= lambda: faceVerify(frame))
    nextBtn.place(x=610,  y=510)




