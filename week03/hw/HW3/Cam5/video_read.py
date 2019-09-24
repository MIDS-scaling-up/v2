import numpy as np
import cv2
import paho.mqtt.client as paho

#sudo docker run -e DISPLAY=$DISPLAY --privileged -v /tmp:/tmp --rm --env QT_X11_NO_MITSHM=1 video python ./video_read.py

broker="172.17.0.1"
port=1883

def on_publish(client, userdata, result):
	print("TX2: Data published")
	pass

client = paho.Client("admin")
client.on_publish = on_publish
client.connect(broker, port)

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
#print('Test!')
cap = cv2.VideoCapture(1)
#print('Video capture successful!')


while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# We don't use the color information, so might as well save space
	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
	
	# Display the resulting frame
	#cv2.imshow('frame',gray)

	# face detection and other logic goes here
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	# gray here is the gray frame you will be getting from a camera
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	
	for (x,y,w,h) in faces:
		# logic for face
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)  
		roi_gray = gray[y:y+h, x:x+w]
		
		#cv2.imshow('frame',gray)
 
		rc,png = cv2.imencode('.png', gray)
		msg = png.tobytes()
		#print(msg)
		ret = client.publish("tx2face_topic", msg)

	#Send logic
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()
