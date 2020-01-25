#!/usr/bin/env python 

import numpy as np 
import cv2 as cv 
import os
import time
import paho.mqtt.client as mqtt

cascadeXMLpath = '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml'
face_cascade=cv.CascadeClassifier(cascadeXMLpath)

 # 0 corresponds to the USB camera. Check using ls -lrth /dev/video* or v4l2-ctl --list-devices
cap = cv.VideoCapture(1)

host_ip='172.19.1.3' # docker ip address of the broker
port=1883 # mqtt port
keepalive=60 # timeout
topic="face_detection"
client=mqtt.Client()
client.connect(host_ip,port,keepalive)

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
    grayScale = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)  # convert the frame to grayscale
    faces=face_cascade.detectMultiScale(grayScale,1.3,5)  # detect faces from the frame
    for(x,y,w,h) in faces:
		face = cv.rectangle(grayScale,(x,y),(x+w,y+h),(255,0,0),2)  # cut out the face from the frame
		croppedFace=crop_face(x,y,w,h,face)
		cv.imshow('Video',croppedFace)
		ret,face_png = cv.imencode('.png', croppedFace)
		msg = face_png.tobytes()  # convert to byte stream
                client.publish(topic,msg)
		
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
client.disconnect()
