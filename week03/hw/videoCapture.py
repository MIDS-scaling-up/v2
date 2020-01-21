#!/usr/bin/env python 

import numpy as np 
import cv2 as cv 
face_cascade=cv.CascadeClassifier('/lib/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

 # 0 corresponds to the USB camera. Check using ls -lrth /dev/video* or v4l2-ctl --list-devices
cap = cv.VideoCapture(0)


def crop_face(x,y,w,h,img):
	r = max(w,h)/2
	centerx = x+w/2
	centery = y+h/2
	nx=int(centerx-r)
	ny=int(centery-r)
	nr=int(r*2)
	faceimg=img[ny:ny+nr,nx:nx+nr]
	croppedFrame=cv.resize(faceimg,(720,720))
	return croppedFrame

while(True):
    #Capture frame by frame 
    ret,frame = cap.read()
    # ignore the color information and save spaces
    grayScale = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(grayScale,1.3,5)
    print(len(faces))
    #cv.imshow('Video', grayScale)
    for(x,y,w,h) in faces:
		face = cv.rectangle(grayScale,(x,y),(x+w,y+h),(255,0,0),2)
		croppedFrame=crop_face(x,y,w,h,face)
		cv.imshow('Video',croppedFrame)
		
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

	


cap.release()
cv.destroyAllWindows()

