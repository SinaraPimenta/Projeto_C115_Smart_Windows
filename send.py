
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="test.mosquitto.org" 

#Sensor de Temperatura 
client = mqtt.Client("Smart_Window_Sensors")
client.connect(mqttBroker) 

while True:
    temperature = uniform(-10, 50) #valores adaptados para condições reais
    client.publish("SRS/INATEL/TEMPERATURE", temperature)
    print("Just published " + str(temperature) + " to topic SRS/INATEL/TEMPERATURE")
    
    rain = uniform(0, 100) #valores em porcentagem
    client.publish("SRS/INATEL/RAIN", rain)
    print("Just published " + str(rain) + " to topic SRS/INATEL/RAIN")
    
    co2 = uniform(400, 8192) 
    client.publish("SRS/INATEL/CO2", co2)
    print("Just published " + str(co2) + " to topic SRS/INATEL/CO2")

    time.sleep(3)
