#!/bin/bash -f 

image_name='sgupta/opencv:latest'
container_name='face_detector'

sudo docker run -d \
	--user=root \
	-e DISPLAY=$DISPLAY \
	--name $container_name \
       	--rm --privileged \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $(pwd):/data \
	-v /data/opencv:/lib/opencv \
	-t $image_name \
