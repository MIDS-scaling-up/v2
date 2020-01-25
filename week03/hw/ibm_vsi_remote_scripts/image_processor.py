#!/usr/bin/env python 

import paho.mqtt.client as mqtt
import time
import os

LOCAL_MQTT_HOST="172.18.0.2"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "face_detection"

# PWD on the host machine is mapped to /data in the docker 
msg_dir = "/data/image_files/" # directory on remote cloud instance before sending to object storage bucket
i = 0

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata,msg):
    global i
    i=i+1
    # when message is received, store it in the cloud bucket
    store_msg = msg.payload
    filepath=msg_dir+"img_file"+str(i)
    with open(filepath, 'w') as f:
        f.write(store_msg)
    os.system('nohup s3cmd put -v image_files/img_file1 s3://w251-suhasgupta-hw3 > log.out 2>$1')

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop to maintain network flow
local_mqttclient.loop_forever()
