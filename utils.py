import cv2
from PIL import Image, ImageTk



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