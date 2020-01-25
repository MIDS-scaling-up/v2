#!/bin/bash -f 

image_name='sgupta/opencv:latest'
container_name='face_detector'
network_name='face_detection'

xhost + local:root
sudo docker run -d \
	--user=root \
	-e DISPLAY=$DISPLAY \
	--name $container_name \
        --rm \
        --privileged \
	--network $network_name \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $(pwd):/data \
	-v /usr/share/opencv4/:/usr/share/opencv \
	-t $image_name 
