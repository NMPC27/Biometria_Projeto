import customtkinter as Ctk
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os
import utils
import facedetection
import nfc
import fingerprint

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

        self.vid = vid
        # configure window
        self.title("Biometria")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        self.frame = Ctk.CTkFrame(master=self,width=1100, height=580)
        self.frame.place(x=0, y=0)

        self.entryPage()

    
    def PopUp(self,msg):
        """
        PopUp window with a message

        Args:
            msg (str): Message to display
        """
        pop_up= Ctk.CTkToplevel(self)
        pop_up.geometry("250x150+865+465")
        pop_up.title("Warning")
        label = Ctk.CTkLabel(pop_up, text= msg, font=('Arial',16)).place(x=125,y=75,anchor="center")

    def entryPage(self):
        """
        Page with login and register buttons
        """
        self.user=None

        for widget in self.frame.winfo_children():
            widget.destroy()
            
        loginBtn = Ctk.CTkButton(self.frame , text="Login", command= lambda: self.nfc(register=False))
        loginBtn.place(x=410,  y=280)
        registerBtn = Ctk.CTkButton(self.frame , text="Register", command=lambda: self.nfc(register=True) )
        registerBtn.place(x=610,  y=280)


    
    def nfc(self, register=False):
        """
        NFC page, can be used for login or register, requires the user to use the NFC reader

        Args:
            register (bool, optional): If true, register a new user. Defaults to False.
        """
        #clear frame
        for widget in self.frame.winfo_children():
            widget.destroy()


        #* Please use the NFC reader
        label = Ctk.CTkLabel(self.frame, text="Enter your NFC ID",font=("Arial", 20))
        label.place(x=480, y=40)
        
        nfcImg = Ctk.CTkImage(light_image=Image.open("./img/nfc.png"), size=(300 , 180))
        nfc_label = Ctk.CTkLabel(master=self.frame, image=nfcImg, text='')
        nfc_label.place(x=400, y=200)


        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.entryPage() )
        cancelBtn.place(x=410, y=540)

        nextBtn = Ctk.CTkButton(self.frame , text="Next", state="disabled")
        nextBtn.place(x=610, y=540)


        #*depois ver como se faz o loop para verificar se o nfc foi lido
        #* funciona como teste, dá sempre 1, True
        if register:
            user, success = nfc.nfc_register()
            if success:
                self.user = user
                nextBtn.configure(state="normal")
                nextBtn.configure(command= lambda: self.faceRecognition(register=True))
                
        else:
            user, success = nfc.nfc_login()
            if success:
                self.user = user
                nextBtn.configure(state="normal")
                nextBtn.configure(command= lambda: self.faceRecognition(register=False))
            else:
                self.PopUp("Invalid NFC ID")
        

        # #! TESTS ONLY
        # nextBtn = Ctk.CTkButton(self.frame , text="TEST NEXT", command= lambda: self.faceRecognition())
        # nextBtn.place(x=610,  y=510)
        
        #?override card reader
        self.nfcInput = Ctk.CTkEntry(self.frame, placeholder_text="NFC ID -> put '1' ")
        self.nfcInput.place(x=400, y=200)
        # #! END TESTS ONLY


    def faceRecognition(self, register=False):
        """
        Face recognition page, can be used for login or register, requires the user to use the camera

        Args:
            register (bool, optional): If true, register a new user. Defaults to False.
        """
        #! TESTS ONLY
        nfcinput = self.nfcInput.get() #! CLEAR USER INPUT
        self.user = nfcinput if nfcinput != "" else "1"
        print(self.user)
        #! END TESTS ONLY

        #clear frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        #frame for the video feed
        self.video_label = Ctk.CTkLabel(self.frame, fg_color="transparent", bg_color="transparent", text="")
        self.video_label.place(x=250, y=30)
        self.open_camera(register=True)
        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.entryPage() )
        cancelBtn.place(x=410, y=540)

        nextBtn = Ctk.CTkButton(self.frame , text="Next")
        nextBtn.place(x=610, y=540)

        if register:
            nextBtn.configure(command= lambda: self.registerFace())
        else:
            nextBtn.configure(command= lambda:self.verifyFace())




    #!LIVELINESS é AQUI
    #! o deepface tem uma cena de ler emocoes
    #! vamos gerar random tipo (sorria, cara de mau, etc) e dps ver se a pessoa faz a expressao
    def registerFace(self):
        """	
        Register a face in the database
        """
        user=self.user
        #capture image from video feed
        image = utils.capture_frame(vid, raw=True)
        success, error = facedetection.registerFace(image, user)
        if success:
            self.fingerprint(register=True)
        else:
            self.PopUp(error)

    def verifyFace(self):
        """
        Verify user face
        """
        user=self.user
        #capture image from video feed
        image = utils.capture_frame(vid, raw=True)
        success, error = facedetection.faceVerify(image, user)
        if success:
            self.fingerprint()
        else:
            self.PopUp(error)


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

        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.entryPage())
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

        doneBtn = Ctk.CTkButton(self.frame , text="Done", command= lambda: self.entryPage() )
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

        doneBtn = Ctk.CTkButton(self.frame , text="Done", command= lambda: self.entryPage() )
        doneBtn.place(x=480, y=540)
        self.open_camera()


    def open_camera(self, register = False):
        """
        gets camera frame and puts it on video label, draw green rectangle if registering a new user

        Args:
            register (bool, optional): If true, draw green rectangle. Defaults to False.
        """
        
        camera_frame = utils.capture_frame(vid,raw=True)

        boxes = facedetection.detect_faces(camera_frame)
        for (x,y,w,h) in boxes:
            cv2.rectangle(camera_frame,(x,y),(x+w,y+h),(0,0,255),3)

        if register:
            cv2.rectangle(camera_frame,(X_POS,Y_POS),(WIDTH,HEIGHT),(0,255,0),3)

        camera_frame = utils.convert_to_photoimage(camera_frame)
  
        # put image in the label
        self.video_label.configure(image=camera_frame)
        #repeat every 15ms
        if register:
            self.video_label.after(15, self.open_camera, True)
        else:
            self.video_label.after(15, self.open_camera)



if __name__ == "__main__":
    vid = cv2.VideoCapture(0)
    app = App(vid)
    app.mainloop()