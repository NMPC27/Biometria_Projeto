import cv2
import os
from deepface import DeepFace
from PIL import ImageTk, Image
import utils


#TODO replace with deepface.extract_faces
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

    #!falta ver a box verde
    #posicao ta em face_obj[0] qq coisa


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