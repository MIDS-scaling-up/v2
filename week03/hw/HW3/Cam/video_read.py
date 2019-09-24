import numpy as np
import cv2

#sudo docker run -e DISPLAY=$DISPLAY --privileged -v /tmp:/tmp --rm --env QT_X11_NO_MITSHM=1 video python ./video_read.py

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
print('Test!')
cap = cv2.VideoCapture(1)
#print('Video capture successful!')

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# We don't use the color information, so might as well save space
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
	
	# Display the resulting frame
	#cv2.imshow('frame',gray)

	# face detection and other logic goes here
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	# gray here is the gray frame you will be getting from a camera
	gray = cv.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	
	for (x,y,w,h) in faces:
		# logic for face
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)  
		roi_gray = gray[y:y+h, x:x+w]
 
		rc,png = cv2.imencode('.png', gray)
		msg = png.tobytes()
		print(msg)
	cv2.imshow('img',png)

	#Send logic
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()
