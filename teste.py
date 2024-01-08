import cv2
from math import log
import numpy as np
import PIL.Image as Image
import facedetection

vid = cv2.VideoCapture(2)
_,frame = vid.read()
gamma = 1.0

while True:
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)
    
    boxes = facedetection.detect_faces(frame)
    #adjust  gamma on detected faces
    if len(boxes) > 0:
        for box in boxes:
            x1, y1, width, height = box
            x2 = x1 + width
            y2 = y1 + height
            face = frame[y1:y2, x1:x2]
            #adjust  gamma
            # invGamma = 1.0 / gamma
            # table = np.array([((i / 255.0) ** invGamma) * 255
            #     for i in np.arange(0, 256)]).astype("uint8")
            # face = cv2.LUT(face, table)
            # frame[y1:y2, x1:x2] = face
            
            # convert img to gray
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # compute gamma = log(mid*255)/log(mean)
            mid = 0.5
            mean = np.mean(gray)
            gamma = log(mid*255)/log(mean)
            print(gamma)
            gamma = 1/gamma
            # do gamma correction
            img_gamma1 = np.power(face, gamma).clip(0,255).astype(np.uint8)
            cv2.imshow("frame", img_gamma1)
            
            
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    # cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key == ord('d'):
        gamma += 0.1
        # print(gamma)
    elif key == ord('a'):
        gamma -= 0.1
        # print(gamma)