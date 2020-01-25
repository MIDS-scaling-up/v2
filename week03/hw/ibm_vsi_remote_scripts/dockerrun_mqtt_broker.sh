#!/bin/bash -f 

image_name='alpine_mqtt'
container_name='alpine_mqtt_broker'
network_name='face_detection'

sudo docker run -d \
        --user=root \
        -e DISPLAY=$DISPLAY \
        --name $container_name \
        --rm \
        --privileged \
        --network $network_name \
        -v $(pwd):/data \
        -p 1883:1883 \
        -t $image_name
