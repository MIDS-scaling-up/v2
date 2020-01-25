#!/usr/bin/env python 

import paho.mqtt.client as mqtt 
import time 

LOCAL_MQTT_HOST="172.19.1.3"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face_detection"

REMOTE_MQTT_TOPIC = "face_detection"
REMOTE_MQTT_HOST = "169.44.168.148"
REMOTE_MQTT_PORT = 1883


def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
    # when message is received, forward the message to the cloud host broker"
    #print(msg.topic,":",str(msg.payload))
    forwarding_msg = msg.payload
    remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=forwarding_msg, qos=0, retain=False)


local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

remote_mqttclient=mqtt.Client()
remote_mqttclient.connect(REMOTE_MQTT_HOST,REMOTE_MQTT_PORT,60)

# go into a loop to maintain network flow
local_mqttclient.loop_forever()
remote_mqttclient.loop_forever()
