
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
import database 
from datetime import datetime

mqttBroker ="test.mosquitto.org" 

#Sensor de Temperatura 
client = mqtt.Client("Smart_Window_Sensors")
client.connect(mqttBroker) 

cont = 0

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

    temperature = round(temperature,2)
    rain = int(rain)
    co2 = int(co2)
    if(temperature!=0 and rain!=0 and co2!=0 and cont==60):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        database.sendDB(temperature,rain,co2,timestamp)
        cont = 0
    time.sleep(1)
    cont = cont + 1
