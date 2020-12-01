
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="test.mosquitto.org" 

client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker) 

#while True:
randNumber = uniform(20.0, 21.0)
client.publish("SRS/INATEL/TEMPERATURE", randNumber)
print("Just published " + str(randNumber) + " to topic SRS/INATEL/TEMPERATURE")
time.sleep(1)