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

@app.route('/control/')
def control():
    file = open("control.html", "r") #Leitura do arquivo control.html para exibição deste na página
    html = file.read()
    #Caso o nome da amostra tenha sido enviado para essa página, ela será buscada no BD de modo a retornar
    #os parâmetros necessários (a1,b1,ts,sp,pv,k,tal)
    nome_amostra = str(request.args.get('nome' , "" )) 
    resposta = database.searchSampleDB(nome_amostra)
    if(resposta):
        a1 = resposta['a1']
        b1 = resposta['b1']
        ts = resposta['ts']
        sp = resposta['sp']
        global pv,k,tal,nome
        pv = resposta['pv']
        k = resposta['k']
        tal = resposta['tal']
        nome = resposta['nome']
        #Os valores encontrados no BD, substituem os valores padrão existentes na página web
        #E deste modo, poderão ser usados no plot do gráfico
        html= Avaliar(a1,"0.9930900",html)
        html= Avaliar(b1,"0.0058096",html)
        html= Avaliar(ts,"0.3",html)
        html= Avaliar(sp,"50",html)
        html= Avaliar(k,"valork",html)
        html= Avaliar(tal,"valortal",html)
    else:
        #As próximas renderizações irão usar os valores fixados no input ou um novo valor que venha a ser informado
        a1 = str(request.args.get('A1' , "" ))
        b1 = str(request.args.get('B1' , ""))
        ts = str(request.args.get('Amostragem' , ""))
        sp= str(request.args.get('SetPoint'      , ""))
        k = str(request.args.get('k'    , ""))
        tal = str(request.args.get('tal'    , ""))
    #Os demais campos são obtidos normalmente da página html (não tem relação com o BD)
    os= str(request.args.get('Overshoot'      , ""))
    tm= str(request.args.get('tempo'      , ""))
    modo=str(request.args.get('Modo' , ""))
    p = str(request.args.get('Proporcional'  , ""))
    i = str(request.args.get('Integral'      , ""))
    d = str(request.args.get('Derivativo'    , ""))
    fs = str(request.args.get('fixed_scale'    , "")) #Obtém se o campo escala fixa está selecionado
    ps = str(request.args.get('plot_sample'    , "")) #Obtém se o campo exibir amostras está selecionado
    pa = str(request.args.get('plot_all'    , "")) #Obtém se o campo comparar modos está selecionado
    #Caso algum campo esteja vazio/não foi informado um valor para ele, atribui-se um valor padrão
    if a1=="":
        a1="0.9930900"
    if b1=="":
        b1 = 0.0058096
    if ts=="":
        ts=0.3
    if sp=="":
        sp = 50
    if p=="":
        p = 0
    if p=="kp":
        p=0
    if i=="":
        i = 0
    if i=="ki":
        i = 0
    if d=="":
        d = 0
    if d=="kd":
        d = 0
    if fs=="":
        fs=0
    if ps=="":
        ps=0
    if pa=="":
        pa=0
    if k=="":
        k=1
    if k=="valork":
        k=1
    if tal=="":
        tal=1
    if tal=="valortal":
        tal=1
    if os=="":
        os=15
    if tm=="":
        tm=60
    #Para retenção dos valores nos inputs:
    html= Avaliar(a1,"0.9930900",html)
    html= Avaliar(b1,"0.0058096",html)
    html= Avaliar(ts,"0.3",html)
    html= Avaliar(sp,"50",html)
    html= Avaliar(os,"15",html)
    html= Avaliar(tm,"60",html)
    html= Avaliar(k,"valork",html)
    html= Avaliar(tal,"valortal",html)
    html= Avaliar(p,"kp",html)
    html= Avaliar(i,"ki",html)
    html= Avaliar(d,"kd",html)

    #Armazena ultimo SetPoint para a tela de monitoramento
    global LastSP
    LastSP=float(sp)
    #Chama a função para plotar o gráfico, informando todos valores necessários:
    retorno,timestamp=plotGrafico.plot(modo,float(a1),float(b1),float(ts),float(sp),
 float(p),float(i),float(d),int(fs),int(ps),int(pa),float(os),float(tm),float(k),float(tal),pv,nome)
    #A nova tabela e o novo gráfico são renderizados:
    html=html.replace("table_placeholder",retorno)
    html=html.replace("Results.png",("Results"+timestamp+".png"))
    return html 


if __name__ == '__main__':
  app.run(debug=True)      