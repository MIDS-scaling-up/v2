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
	-v $(pwd):/data \
	-p 1884:1883 \
	-t $image_name
