import cv2
import os
from deepface import DeepFace
from PIL import ImageTk, Image
import utils
import dlib
from imutils import face_utils



dlib_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("./model/shape_predictor_68_face_landmarks.dat")

def detect_faces(img):
        """
        Detects faces in an image and returns the coordinates of the bounding boxes
        
        Parameters:
            img (Matlike): Image to detect faces in
            
        Returns:
            list: List of bounding boxes
        """
        try:
            face_obj=DeepFace.extract_faces(img_path = img, detector_backend = 'opencv')
        except:
            return []
        
        facial_areas = [face["facial_area"] for face in face_obj]
        return [[face["x"], face["y"], face["w"], face["h"]] for face in facial_areas]


def registerFace(image,user, average):
    """
    Registers a face in the database

    Args:
        image (Matlike): Image to register
        user (str): User ID
        average (float): Average of the eye aspect ratio
    """
    
    #tell deepface to find faces
    face_obj=DeepFace.extract_faces(img_path = image, detector_backend = 'retinaface')
    
    if len(face_obj) == 0:
        return False, "No face detected"
    if len(face_obj) > 1:
        return False, "More than one face detected"

    #face must be around green box
    X_POS=187 -30
    Y_POS=97 - 30
    WIDTH=483 + 30
    HEIGHT=483 + 30

    facial_area = face_obj[0]["facial_area"]
    if facial_area["x"] < X_POS or facial_area["y"] < Y_POS or facial_area["x"]+facial_area["w"] > X_POS+WIDTH or facial_area["y"]+facial_area["h"] > Y_POS+HEIGHT:
        return False, "Face not inside the box"

    if blink(image, average)[0]:
        return False, "Eyes closed!"
    
    #save the selfie
    image = utils.convert_to_photoimage(image)      
    image = ImageTk.getimage(image)

    #mirror image, because the camera is mirrored
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    
    #return true if user is new and false if user already exists
    if not os.path.exists("./db/"+user):
        os.mkdir("./db/"+user)
    
    #?delte old user image or skip and say already exists?
    else:
        pass
    
    image.save("./db/"+user+"/user.png")
    return True, "User registered"
    


def faceVerify(image,user):
    """
    Verifies a face in the database

    Args:
        image (Matlike): Image to verify
        user (str): User ID
    """



    result = DeepFace.verify(img1_path = image, img2_path = f"./db/{user}/user.png", model_name = 'Facenet')
    print(f"result: {result['verified']}")

    if result["verified"]:
        return True, "Face recognized"
    else:
        return False, "Face not recognized"


def get_eyes_aspect_ratio(image):
    """
    Calculates the eye aspect ratio

    Args:
        image (Matlike): Image to calculate the eye aspect ratio

    Returns:
        float: Eye aspect ratio
    """
    # img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = dlib_detector(image, 0)
    if len(faces) == 0 or len(faces) > 1:
        return 0
    
    face = faces[0]
    landmarks = landmark_predictor(image, face)
    landmarks = face_utils.shape_to_np(landmarks)

    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]

    left_eye_aspect_ratio = utils.eye_aspect_ratio(left_eye)
    right_eye_aspect_ratio = utils.eye_aspect_ratio(right_eye)

    eye_aspect_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2
    return (eye_aspect_ratio, left_eye, right_eye)


def blink(image, average):
    """
    Verifies if blink is detected

    Args:
        image (Matlike): Image to verify
        average (float): Average of the eye aspect ratio

    Returns:
        int: 1 if blink detected, 0 otherwise
        
    """
    eye_aspect_ratio, left_eye, right_eye = get_eyes_aspect_ratio(image)
    # print(eye_aspect_ratio)
    if eye_aspect_ratio < average * 0.8:
        return 1, left_eye, right_eye
    else:
        return 0, left_eye, right_eye

