#!/usr/bin/env python 

import os 
import time 
import paho.mqtt.client as mqtt 

host_ip = '127.0.0.1' # loopback address for host machine
port = 1883
keepalive=60 # timeout
topic="face_detection"

broker=mqtt.Client()
broker.connect(host_ip,port,keepalive)
broker.subscribe(topic,0)
