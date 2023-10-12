import customtkinter as Ctk
import cv2
import face_detection
from PIL import Image, ImageTk

Ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
Ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# create a class for the app, it will have a video feed from the camera and a bottom bar with 2 buttons
#Ctk works like tkinter, but with a few more features and styling options
class App(Ctk.CTk):
    def __init__(self, vid):
        super().__init__()
        self.vid = vid
        # configure window
        self.title("Cam_FaceRecognition.py")
        self.geometry(f"{1100}x{580}")

        #frame for the video feed
        self.video_label = Ctk.CTkLabel(self, fg_color="transparent", bg_color="transparent", text="")
        self.video_label.pack(expand=True, fill="both")
        

        #create a frame and put it on the bottom as a bottom bar with 2 buttons
        self.bottom_bar = Ctk.CTkFrame(self, height=300)
        #pack it to the bottom
        self.bottom_bar.pack(side="bottom", fill="x")
        
        
        #button container
        self.button_container = Ctk.CTkFrame(self.bottom_bar, fg_color="transparent",height=40)
        self.button_container.pack( expand=True)
        #2 buttons packed next to each other on the container
        self.btn1 = Ctk.CTkButton(self.button_container, text="Start", command=self.start)
        self.btn1.pack(side="left",padx=(0,50))
        
        self.btn2 = Ctk.CTkButton(self.button_container, text="Stop", command=self.stop)
        self.btn2.pack(side="left", padx=50)

        self.open_camera()
        
    def start(self):
        print("Start button pressed")
        #get image currently in the label 
        image = self.video_label.cget("image")
        #save it
        PilImage = ImageTk.getimage(image)
        PilImage.save("test.png")
        
    def stop(self):
        print("Stop button pressed")
        
    def open_camera(self):
  
        # Capture the video frame by frame
        _, frame = vid.read()
    
        # Convert image from one color space to other
        opencv_image = frame

        #detect faces on the image
        boxes = face_detection.detect_faces(opencv_image)

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
    
        
        
        
if __name__ == "__main__":
    vid = cv2.VideoCapture(0)
    
    app = App(vid)
    #bind escape key to quit and release the camera
    app.bind("<Escape>", lambda e: [vid.release(), app.quit()])
    app.mainloop()