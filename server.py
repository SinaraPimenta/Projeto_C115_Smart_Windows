from flask import Flask,request,send_from_directory
import os
from flask import  flash,  redirect, url_for, render_template
import paho.mqtt.client as mqtt
import time  

ALLOWED_EXTENSIONS = {'txt'}
app = Flask(__name__)
LastSP=999
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 

#Variáveis globais
pv = []
k = 0
tal = 0
nome = None

temperatura = '0'

def on_message(client, userdata, message):
  print("received message: " ,str(message.payload.decode("utf-8")))
  global temperatura
  temperatura = str(message.payload.decode("utf-8")) 
  temperatura = round(float(temperatura),2)
  print(temperatura)

mqttBroker ="test.mosquitto.org"
client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 

client.loop_start()
client.subscribe("SRS/INATEL/TEMPERATURE")
client.on_message=on_message 
#client.loop_stop()

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
  
  data = {'temp': temperatura, 'chuva': '50%', 'co2':'1000ppm'}
  return render_template('dashboard.html', data=data)

if __name__ == '__main__':
  app.run(debug=True)      