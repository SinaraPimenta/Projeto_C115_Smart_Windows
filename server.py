from flask import Flask,request,send_from_directory
import os
from flask import  flash,  redirect, url_for, render_template
import paho.mqtt.client as mqtt
import time 
import database 

app = Flask(__name__)

#Variáveis globais
temperatura = '0'
chuva = '0'
co2 = '0'

def on_messageTemp(client, userdata, message):
  print("received messageTemp: " ,str(message.payload.decode("utf-8")))
  global temperatura
  temperatura = str(message.payload.decode("utf-8")) 
  temperatura = round(float(temperatura),2)

def on_messageRain(client, userdata, message):
  print("received messageRain: " ,str(message.payload.decode("utf-8")))
  global chuva
  chuva = str(message.payload.decode("utf-8")) 
  chuva = round(float(chuva),0)

def on_messageCO2(client, userdata, message):
  print("received messageCO2: " ,str(message.payload.decode("utf-8")))
  global co2
  co2 = str(message.payload.decode("utf-8")) 
  co2 = round(float(co2),0)

### topic message
def on_message(mosq, obj, msg):
  print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def receive():
  mqttBroker ="test.mosquitto.org"
  client = mqtt.Client("Smartphone")
  client.connect(mqttBroker) 
  client.loop_start()
  client.message_callback_add('SRS/INATEL/TEMPERATURE', on_messageTemp)
  client.message_callback_add('SRS/INATEL/RAIN', on_messageRain)
  client.message_callback_add('SRS/INATEL/CO2', on_messageCO2)
  client.on_message = on_message
  client.subscribe("SRS/INATEL/#")

#Função para substituição de valores na página html
def Avaliar(var,value,html):
  if str(var)!=str(value):
    html=html.replace(('"'+str(value)+'"'),('"'+str(var)+'"'))
  return html

@app.route('/')
def index():
  return '<h2>Main</h2> <br> redirecting to /control... <meta http-equiv = "refresh" content = "1; url = /control/" />'

@app.route('/dashboard/')
def control():
  receive()    
  if(temperatura!=0 and chuva!=0 and co2!=0):
    database.sendDB(temperatura,chuva,co2)
  temperaturas,chuvas,co2s = database.searchDB()  
  data = {'temp': temperatura, 'chuva': chuva, 'co2': co2,'arrayTemp':temperaturas,
  'arrayChuva':chuvas,'arrayCO2':co2s}
  return render_template('dashboard.html', data=data)

if __name__ == '__main__':
  app.run(debug=True)      