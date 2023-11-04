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
            face_obj=DeepFace.extract_faces(img_path = img, detector_backend = 'ssd')
        except:
            return []
        
        facial_areas = [face["facial_area"] for face in face_obj]
        return [[face["x"], face["y"], face["w"], face["h"]] for face in facial_areas]


def registerFace(image,user):
    """
    Registers a face in the database

    Args:
        image (Matlike): Image to register
        user (str): User ID
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

    if blink(image):
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
    face_obj=DeepFace.extract_faces(img_path = image, detector_backend = 'retinaface')


    if len(face_obj) == 1:
        result = DeepFace.verify(img1_path = image, img2_path = f"./db/{user}/user.png", model_name = 'Facenet')
        print(f"result: {result['verified']}")

        if result["verified"]:
            return True, "Face recognized"
        else:
            return False, "Face not recognized"
    else:
        return False , "Face not detected or more than one face detected"
    

def blink(image):
    """
    Verifies if blink is detected

    Args:
        image (Matlike): Image to verify

    Returns:
        int: 1 if blink detected, 0 otherwise
    """
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = dlib_detector(img_gray, 0)
    if len(faces) == 0 or len(faces) > 1:
        return 0
    
    face = faces[0]
    landmarks = landmark_predictor(img_gray, face)
    landmarks = face_utils.shape_to_np(landmarks)

    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]

    left_eye_aspect_ratio = utils.eye_aspect_ratio(left_eye)
    right_eye_aspect_ratio = utils.eye_aspect_ratio(right_eye)

    eye_aspect_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2
    if eye_aspect_ratio < 0.2:
        return 1
    else:
        return 0

