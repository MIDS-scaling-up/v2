import paho.mqtt.client as mqtt

# Subscriber

def on_connect(client, userdata, flags, a):
  print("Connected with result code "+str(a))
  client.subscribe("_tx2/webcam/#", qos=0)

def on_message(client, userdata, msg):
  client_pub.publish(msg.topic, msg.payload, qos=1)
  print ("message is published")

while True:
  try:
    client_sub = mqtt.Client()
    client_sub.connect("mosquitto",1883, 10)

    client_pub = mqtt.Client()
    client_pub.connect("169.61.86.171",1883, 20)

    client_sub.on_connect = on_connect
    client_sub.on_message = on_message
    
  except:
    continue
