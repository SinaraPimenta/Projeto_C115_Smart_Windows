
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="test.mosquitto.org" 

#Sensor de Temperatura 
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker) 

while True:
    randNumber = uniform(-10, 50) #valores adaptados para condições reais
    client.publish("SRS/INATEL/TEMPERATURE", randNumber)
    print("Just published " + str(randNumber) + " to topic SRS/INATEL/TEMPERATURE")
    time.sleep(3)
