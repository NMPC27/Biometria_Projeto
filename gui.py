import customtkinter as Ctk
import cv2
import face_detection
from PIL import Image, ImageTk
from deepface import DeepFace
import threading

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
        



        self.open_camera_thread()
        
    def start(self):
        print("Start button pressed")
        #get image currently in the label 
        image = self.video_label.cget("image")
        #save it
        PilImage = ImageTk.getimage(image)
        PilImage.save("test.png")
        result = DeepFace.verify(img1_path = "cunha.png", img2_path = "test.png")
        
        print(result)

        
    def stop(self):
        print("Stop button pressed")
    
    def open_camera_thread(self):
        #open camera in a thread
        threading.Thread(target=self.open_camera).start()

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