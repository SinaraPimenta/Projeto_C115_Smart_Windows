import pymongo
from datetime import datetime

#Conexão com o BD
cliente = pymongo.MongoClient("mongodb+srv://admin:rJEONpT0DYQ7Lntp@clusterc115.28mlu.mongodb.net/SmartWindows?retryWrites=true&w=majority")
db = cliente["SmartWindows"] #nome do banco
collection = db["DadosSensores"] #nome da coleção
temperaturas = []
chuvas = []
co2s = []
tempos = []

#Função para salvar a amostra no BD
def sendDB(temperatura,chuva,co2,timestamp):
  dados = {"temperatura": temperatura, "chuva": chuva, "co2": co2,"timestamp":timestamp}
  collection.insert_one(dados)

#Função para retornar as amostras salvas no BD
def searchDB():
  temperaturas.clear()
  chuvas.clear()
  co2s.clear()
  tempos.clear()
  resposta = collection.find().sort([("timestamp", -1)]).limit(6)  #traz os últimos 6 registros 
  for data in resposta: 
    temperaturas.append(data['temperatura'])
    chuvas.append(data['chuva'])
    co2s.append(data['co2'])
    data_hora = datetime.fromtimestamp(data['timestamp'])
    data_hora = data_hora.strftime("%d/%m/%Y %H:%M")
    tempos.append(data_hora)
  return temperaturas,chuvas,co2s,tempos