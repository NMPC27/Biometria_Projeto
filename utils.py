import cv2
from PIL import Image, ImageTk
from scipy.spatial import distance as dist


def convert_to_photoimage(camera_frame):
    #convert to good color space
    camera_frame = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
    
    # Capture the latest frame and transform to image
    camera_frame = Image.fromarray(camera_frame)
    
    #mirror image
    camera_frame = camera_frame.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Convert captured image to tkinter photoimage
    photo_image = ImageTk.PhotoImage(image=camera_frame)
    return photo_image

def capture_frame(vid, raw=False):
    """
    captures frame from camera
    """
    # Capture the video frame by frame
    _, camera_frame = vid.read()

    if raw:
        return camera_frame
    
    return convert_to_photoimage(camera_frame)


def eye_aspect_ratio(eye):


    # calculate the vertical distances 
    y1 = dist.euclidean(eye[1], eye[5]) 
    y2 = dist.euclidean(eye[2], eye[4]) 
  
    # calculate the horizontal distance 
    x1 = dist.euclidean(eye[0], eye[3]) 
  
    # calculate the EAR 
    EAR = (y1+y2) / x1 
    return EAR 