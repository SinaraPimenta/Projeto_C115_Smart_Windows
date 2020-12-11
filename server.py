from flask import Flask,request,send_from_directory
import os
from flask import  flash,  redirect, url_for, render_template
import paho.mqtt.client as mqtt
from datetime import datetime
import database 

app = Flask(__name__)

#Variáveis globais
temperatura = 0
chuva = 0
co2 = 0
estadoJanela = '0'
verificacao = '' 

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

def on_messageStateW(client, userdata, message):
  print("received messageStateW: " , message.payload.decode("utf-8"))
  global estadoJanela
  estadoJanela = str(message.payload.decode("utf-8")) 

def on_messageStateWUsers(client, userdata, message):
  print("received messageStateWUsers: " , message.payload.decode("utf-8"))
  global verificacao
  verificacao = str(message.payload.decode("utf-8")) 

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
  client.message_callback_add('SRS/INATEL/STATEWINDOWS', on_messageStateW)
  client.message_callback_add('SRS/INATEL/STATEWINDOWSUSERS', on_messageStateWUsers)
  client.on_message = on_message
  client.subscribe("SRS/INATEL/#")

@app.route('/dashboard/')
def control():
  receive()
  now = datetime.now()
  now = now.strftime("%d/%m/%Y %H:%M")  
  temperaturas,chuvas,co2s,tempos,estados = database.searchDB()
  global verificacao, estadoJanela
  estado = estadoJanela
  verifica = verificacao
  if(verifica == '' or verifica == 'AUTO'):
    janela = estado
  else:
    janela = verifica
  data = {'temp': temperatura, 'chuva': chuva, 'co2': co2,'tempoAgora': now,'estado':janela,'arrayTemp':temperaturas,
  'arrayChuva':chuvas,'arrayCO2':co2s,'arrayTempo':tempos,'arrayEstados':estados}
  return render_template('dashboard.html', data=data)

if __name__ == '__main__':
  app.run(debug=True)    