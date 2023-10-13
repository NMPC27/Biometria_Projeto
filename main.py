import customtkinter as Ctk
import cv2
import face_detection
from PIL import Image, ImageTk
from deepface import DeepFace
import threading

from loginPage import *
from registerPage import *


Ctk.set_appearance_mode("System")   
Ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(Ctk.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Biometria")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)


        self.frame = Ctk.CTkFrame(master=self,width=1100, height=580)
        self.frame.place(x=0,  y=0)
        self.loginBtn = Ctk.CTkButton(self.frame , text="Login", command= lambda: login(self.frame))
        self.loginBtn.place(x=410,  y=280)
        self.registerBtn = Ctk.CTkButton(self.frame , text="Register", command=lambda: register(self.frame))
        self.registerBtn.place(x=610,  y=280)












if __name__ == "__main__":
    app = App()
    app.mainloop()