import numpy as np
import cv2
import time


def output_faces(gray):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print (len(faces))
    for (x, y, w, h) in faces:
#        yield (x, y, w, h)
        print (x)
        

if __name__ == '__main__':
    # Use the pre-trained Face Cascade Classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
    cap = cv2.VideoCapture(1)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # We don't use the color information, so might as well save space
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # face detection and other logic goes here
        output_faces(gray)
        time.sleep(1)

