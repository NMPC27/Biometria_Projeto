import cv2
from PIL import Image


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