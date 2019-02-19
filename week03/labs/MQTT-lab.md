### A Nano-lab on MQTT 
MQTT - http://mqtt.org/ is a lightweight messaging protocol for the Internet of Things. What are the QoS 0,1, and 2 that MQTT enables?

### Mosquitto
Perhaps the most popular OpenSource MQTT toolkit is called Mosquitto.  Let's get it installed.  
On your Jetson, do this:
```
sudo apt-get update
sudo apt-get install mosquitto-clients
```

### Subscribing to messages on an MQTT Cloud Broker
At this point, we will use our new VM to subscribe to the public topic tree on an MQTT bus
```
mosquitto_sub -t /applications/in/+/public/# -h 169.44.201.108
```
### Questions
What do the + and # in the line above stand for? Can you recognize some of the messages?  What is their meaning?
