#!/bin/bash -f 

xhost + local:root
xterm -hold -e 'docker exec alpine_mqtt_broker /bin/bash -c "mosquitto"' &
