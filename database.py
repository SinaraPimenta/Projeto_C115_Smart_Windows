import pymongo

#Conexão com o BD
cliente = pymongo.MongoClient("mongodb+srv://admin:rJEONpT0DYQ7Lntp@clusterc115.28mlu.mongodb.net/SmartWindows?retryWrites=true&w=majority")
db = cliente["SmartWindows"] #nome do banco
collection = db["DadosSensores"] #nome da coleção
temperaturas = []
chuvas = []
co2s = []

#Função para salvar a amostra no BD
def sendDB(temperatura,chuva,co2):
  dados = {"temperatura": temperatura, "chuva": chuva, "co2": co2}
  collection.insert_one(dados)

#Função para retornar as amostras salvas no BD
def searchDB():
  temperaturas.clear()
  chuvas.clear()
  co2s.clear()
  resposta = collection.find() 
  for data in resposta: 
    temperaturas.append(data['temperatura'])
    chuvas.append(data['chuva'])
    co2s.append(data['co2'])
  return temperaturas,chuvas,co2s