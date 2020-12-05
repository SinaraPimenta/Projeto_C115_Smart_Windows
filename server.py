from flask import Flask,request,send_from_directory
import os
from flask import  flash,  redirect, url_for

ALLOWED_EXTENSIONS = {'txt'}
app = Flask(__name__)
LastSP=999
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 

#Variáveis globais
pv = []
k = 0
tal = 0
nome = None

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
    file = open("dashboard.html", "r") #Leitura do arquivo control.html para exibição deste na página
    html = file.read()
    return html 


if __name__ == '__main__':
  app.run(debug=True)      