import numpy as np
import cv2 as cv
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# gray here is the gray frame you will be getting from a camera
gray = cv.cvtColor(gray, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
	# your logic goes here; for instance
	# cut out face from the frame.. 
	# rc,png = cv2.imencode('.png', face)
	# msg = png.tobytes()
	# ...
