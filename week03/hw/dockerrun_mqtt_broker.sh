#!/bin/bash -f 

image_name='alpine_mosquitto'
container_name='alpine_mqtt_broker'
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
	-p 1884:1883 \
	-ti $image_name
