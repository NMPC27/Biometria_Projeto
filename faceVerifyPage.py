import customtkinter as Ctk
import cv2
import face_detection
from PIL import Image, ImageTk
from deepface import DeepFace


vid = cv2.VideoCapture(0)


def faceVerify(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    #frame for the video feed
    video_label = Ctk.CTkLabel(frame, fg_color="transparent", bg_color="transparent", text="")
    video_label.place(x=0, y=0)
    cancelBtn = Ctk.CTkButton(frame , text="Cancel", command=lambda: print("not implemented"))
    cancelBtn.place(x=410,  y=300)

    open_camera(video_label)


def detect_faces(img):
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

def open_camera(video_label):
    
  
    # Capture the video frame by frame
    _, frame = vid.read()

    print(frame)

    # Convert image from one color space to other
    opencv_image = frame

    #detect faces on the image
    boxes = detect_faces(opencv_image)

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
    video_label.configure(image=photo_image)

    print("frame")

    #repeat every 15ms
    video_label.after(15, open_camera(video_label))