import customtkinter as Ctk
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os

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

        self.loginPage()


    def loginPage(self):
        self.user=None

        for widget in self.frame.winfo_children():
            widget.destroy()
            
        loginBtn = Ctk.CTkButton(self.frame , text="Login", command= lambda: self.nfc())
        loginBtn.place(x=410,  y=280)
        registerBtn = Ctk.CTkButton(self.frame , text="Register", command=lambda: self.registerNFC() )
        registerBtn.place(x=610,  y=280)


    def nfc(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        allowNext = "disabled"

        label = Ctk.CTkLabel(self.frame, text="Put NFC",font=("Arial", 20))
        label.place(x=480, y=40)

        nfcImg = Ctk.CTkImage(light_image=Image.open("./img/nfc.png"), size=(300 , 180))
        nfc_label = Ctk.CTkLabel(master=self.frame, image=nfcImg, text='')
        nfc_label.place(x=400, y=200)


        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.loginPage() )
        cancelBtn.place(x=410, y=540)
        nextBtn = Ctk.CTkButton(self.frame , text="Next", state=allowNext, command= lambda: self.faceRecognition() )
        nextBtn.place(x=610, y=540)

        #! TESTS ONLY
        nextBtn = Ctk.CTkButton(self.frame , text="TEST NEXT", command= lambda: self.faceRecognition())
        nextBtn.place(x=610,  y=510)

        self.nfcInput = Ctk.CTkEntry(self.frame, placeholder_text="NFC ID -> put '1' ")
        self.nfcInput.place(x=400, y=200)
        #! END TESTS ONLY



    def faceRecognition(self):
        #! TESTS ONLY
        self.user= self.nfcInput.get() #! CLEAR USER INPUT
        print(self.user)
        #! END TESTS ONLY

        for widget in self.frame.winfo_children():
            widget.destroy()

        #frame for the video feed
        self.video_label = Ctk.CTkLabel(self.frame, fg_color="transparent", bg_color="transparent", text="")
        self.video_label.place(x=250, y=30)

        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.loginPage() )
        cancelBtn.place(x=410, y=540)
        authBtn = Ctk.CTkButton(self.frame , text="Authenticate", command= lambda: self.faceVerify() )
        authBtn.place(x=610, y=540)

        self.open_camera()


    def open_camera(self):
        # Capture the video frame by frame
        _, frame = vid.read()
    
        # Convert image from one color space to other
        opencv_image = frame

        #detect faces on the image
        boxes = self.detect_faces(opencv_image)

        for (x,y,w,h) in boxes:
            cv2.rectangle(opencv_image,(x,y),(x+w,y+h),(0,0,255),3)
            
        #convert to good color space
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        
        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        #mirror it
        captured_image = captured_image.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)
     
        # Configure image in the label
        self.video_label.configure(image=photo_image)
    
        #repeat every 15ms
        self.video_label.after(15, self.open_camera)


    def detect_faces(self,img):
        """
        Detects faces in an image and returns the coordinates of the bounding boxes
        
        Parameters:
            img (n
            
        Returns:
            list: List of bounding boxes
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Load the cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        return faces


    def faceVerify(self):
        image = self.video_label.cget("image")
        #save it
        PilImage = ImageTk.getimage(image)
        PilImage.save("tmp.png")
        result = DeepFace.verify(img1_path = "./db/"+self.user+"/user.png", img2_path = "tmp.png") #! CLEAN USER INPUT

        print("result: "+str(result["verified"])+" || original: ./db/"+self.user+"/user.png  <=> ./tmp.png" )

        if result["verified"]:
            self.fingerprint()

    
    def fingerprint(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        allowNext = "disabled"

        fingerImg = Ctk.CTkImage(light_image=Image.open("./img/finger.png"), size=(256 , 256))
        finger_label = Ctk.CTkLabel(master=self.frame, image=fingerImg, text='')
        finger_label.place(x=422, y=162)

        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.loginPage())
        cancelBtn.place(x=410, y=540)
        nextBtn = Ctk.CTkButton(self.frame , text="Next", state=allowNext, command= lambda: self.userPage() )
        nextBtn.place(x=610, y=540)

        #! TESTS ONLY
        nextBtn = Ctk.CTkButton(self.frame , text="TEST NEXT", command= lambda: self.userPage())
        nextBtn.place(x=610,  y=510)
        

    def userPage(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = Ctk.CTkLabel(self.frame, text="Authentication Successful!", text_color="green",font=("Arial", 20))
        label.place(x=450, y=40)

        userImg = Ctk.CTkImage(light_image=Image.open("./img/profile.png"), size=(256 , 256))
        user_label = Ctk.CTkLabel(master=self.frame, image=userImg, text='')
        user_label.place(x=422, y=162)

        doneBtn = Ctk.CTkButton(self.frame , text="Done", command= lambda: self.loginPage() )
        doneBtn.place(x=480, y=540)

    def PopUp(self,msg):
        pop_up= Ctk.CTkToplevel(self)
        pop_up.geometry("250x150+865+465")
        pop_up.title("Warning")
        label = Ctk.CTkLabel(pop_up, text= msg, font=('Arial',16)).place(x=125,y=75,anchor="center")

    ###############################
    #        REGISTER             #
    ###############################

    def registerNFC(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        allowNext = "disabled"

        label = Ctk.CTkLabel(self.frame, text="Put NFC",font=("Arial", 20))
        label.place(x=480, y=40)

        nfcImg = Ctk.CTkImage(light_image=Image.open("./img/nfc.png"), size=(300 , 180))
        nfc_label = Ctk.CTkLabel(master=self.frame, image=nfcImg, text='')
        nfc_label.place(x=400, y=200)


        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.loginPage() )
        cancelBtn.place(x=410, y=540)
        nextBtn = Ctk.CTkButton(self.frame , text="Next", state=allowNext, command= lambda: self.takePic() )
        nextBtn.place(x=610, y=540)

        #! TESTS ONLY
        nextBtn = Ctk.CTkButton(self.frame , text="TEST NEXT", command= lambda: self.takePic())
        nextBtn.place(x=610,  y=510)

        self.registNFC = Ctk.CTkEntry(self.frame, placeholder_text="NFC ID -> put '1' ")
        self.registNFC.place(x=400, y=200)
        #! END TESTS ONLY

    
    def takePic(self):
        #! TESTS ONLY
        self.user= self.registNFC.get() #! CLEAR USER INPUT
        print("USER ID:",self.user)
        #! END TESTS ONLY

        for widget in self.frame.winfo_children():
            widget.destroy()

        label = Ctk.CTkLabel(self.frame, text="Take a picture",font=("Arial", 20))
        label.place(x=480, y=40)

        self.video_label = Ctk.CTkLabel(self.frame, text='')
        self.video_label.place(x=250, y=30)

        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.loginPage() )
        cancelBtn.place(x=410, y=540)
        nextBtn = Ctk.CTkButton(self.frame , text="Take Pic", command= lambda: self.registerFace() )
        nextBtn.place(x=610, y=540)

        self.open_camera_register()

    def open_camera_register(self):
        # Capture the video frame by frame
        _, frame = vid.read()
    
        # Convert image from one color space to other
        opencv_image = frame

        #detect faces on the image
        boxes = self.detect_faces(opencv_image)
        self.boxes = boxes

        for (x,y,w,h) in boxes:
            cv2.rectangle(opencv_image,(x,y),(x+w,y+h),(0,0,255),3)

        cv2.rectangle(opencv_image,(X_POS,Y_POS),(WIDTH,HEIGHT),(0,255,0),3)

        #cv2.rectangle(opencv_image,(MAX_X,MAX_Y),(MAX_WIDTH,MAX_HEIGHT),(0,0,0),3)
        #cv2.rectangle(opencv_image,(MIN_X,MIN_Y),(MIN_WIDTH,MIN_HEIGHT),(255,0,0),3)
            
        #convert to good color space
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        
        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        #mirror it
        captured_image = captured_image.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)
     
        # Configure image in the label
        self.video_label.configure(image=photo_image)
    
        #repeat every 15ms
        self.video_label.after(15, self.open_camera_register)

    def registerFace(self):
        
        if len(self.boxes) == 1:
            if (    (self.boxes[0][0]<= MIN_X and self.boxes[0][0] >= MAX_X) and 
                    (self.boxes[0][1]<= MIN_Y and self.boxes[0][1] >= MAX_Y) and 
                    (self.boxes[0][0]+self.boxes[0][2]>= MIN_WIDTH and self.boxes[0][2] <= MAX_WIDTH) and 
                    (self.boxes[0][1]+self.boxes[0][3]>= MIN_HEIGHT and self.boxes[0][3] <= MAX_HEIGHT) ):

                image = self.video_label.cget("image")
                #save it
                PilImage = ImageTk.getimage(image)
                os.mkdir("./db/"+self.user) 
                PilImage.save("./db/"+self.user+"/user.png")
                
                self.registerFingerprint()

            else:
                self.PopUp("Please, take a picture \n with your face in the box")
        else:
            self.PopUp("Please, take a picture \n with only one face")


    
    def registerFingerprint(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        allowNext = "disabled"

        fingerImg = Ctk.CTkImage(light_image=Image.open("./img/finger.png"), size=(256 , 256))
        finger_label = Ctk.CTkLabel(master=self.frame, image=fingerImg, text='')
        finger_label.place(x=422, y=162)

        cancelBtn = Ctk.CTkButton(self.frame , text="Cancel", command=lambda: self.loginPage())
        cancelBtn.place(x=410, y=540)
        nextBtn = Ctk.CTkButton(self.frame , text="Next", state=allowNext, command= lambda: self.registDone() )
        nextBtn.place(x=610, y=540)

        #! TESTS ONLY
        nextBtn = Ctk.CTkButton(self.frame , text="TEST NEXT", command= lambda: self.registDone())
        nextBtn.place(x=610,  y=510)

    def registDone(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = Ctk.CTkLabel(self.frame, text="Regist Successful!", text_color="green",font=("Arial", 20))
        label.place(x=450, y=40)

        userImg = Ctk.CTkImage(light_image=Image.open("./img/register.png"), size=(256 , 256))
        user_label = Ctk.CTkLabel(master=self.frame, image=userImg, text='')
        user_label.place(x=422, y=162)

        doneBtn = Ctk.CTkButton(self.frame , text="Done", command= lambda: self.loginPage() )
        doneBtn.place(x=480, y=540)




if __name__ == "__main__":
    vid = cv2.VideoCapture(0)
    app = App(vid)
    app.mainloop()