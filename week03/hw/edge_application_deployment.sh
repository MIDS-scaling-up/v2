#!/bin/bash -f 

network_name='face_detection'
xhost + local:root

# Deploy the mosquitto broker container 
image_name='alpine_mosquitto'
container_name='alpine_mqtt_broker'
sudo docker run -d \
	--user=root \
	-e DISPLAY=$DISPLAY \
	--name $container_name \
    --rm \
    --privileged \
	--network $network_name \
	-v $(pwd):/data \
	-p 1884:1883 \
	--ip 172.19.1.3 \
	-t $image_name


# Deploy the mosquitto message forwarder container
image_name="alpine_mosquitto"
container_name="alpine_mqtt_forwarder"
sudo docker run -d \
	--user=root \
	-e DISPLAY=$DISPLAY \
	--name $container_name \
    --rm \
    --privileged \
	--network $network_name \
	-v $(pwd):/data \
	-p 1885:1883 \
	--ip 172.19.1.2\
	-t $image_name



# Deploy the opencv container 
container_name='face_detector'
image_name='sgupta/opencv:latest'
sudo docker run -d \
	--user=root \
	-e DISPLAY=$DISPLAY \
	--name $container_name \
    --rm \
    --privileged \
	--network $network_name \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $(pwd):/data \
	-p 1886:1883 \
	--ip 172.19.1.1\
	-v /usr/share/opencv4/:/usr/share/opencv \
	-t $image_name 
	
# inspect the network
sudo docker network inspect $network_name


