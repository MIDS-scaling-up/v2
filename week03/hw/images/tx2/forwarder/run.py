import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("_tx2/webcam/#", qos=0)

def on_message(client, userdata, msg):
  client_pub.publish(msg.topic, msg.payload, qos=1)
  print ("message published")

while True:
  try:
    client_sub = mqtt.Client()
    client_sub.connect("mosquitto",1883, 10)

    client_pub = mqtt.Client()
    client_pub.connect("158.85.191.118",1883, 20)

    client_sub.on_connect = on_connect
    client_sub.on_message = on_message
    
  except:
    continue
