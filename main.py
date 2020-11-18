
from flask import Flask, render_template, jsonify
import json
app = Flask(__name__)

@app.route('/')
def dashBoard():
  infoDiaria = readFile()
  soFar = currentlyState(infoDiaria)
  config = {'Area de plantio': getData('AreaDestinadaAoPlantioEmkm2'), 'Data': infoDiaria[0]['Data']}
  return render_template('index.html', daily=infoDiaria, soFar=soFar, config=config)

def readFile():
  f = open('./static/requisicoes.txt', 'r')
  lista = []
  for line in f:
    lista.append(json.loads(line))
  return lista

def currentlyState(infoDiaria):
  qtdDias = len(infoDiaria)
  qtdFoiIrrigado = 0
  for i in infoDiaria:
    qtdFoiIrrigado += i['Quantidade de agua a regar no dia']

  qtdIrrigadoSemSolucao = qtdDias * 3
  qtdAguaEconomizada = qtdIrrigadoSemSolucao - qtdFoiIrrigado
  qtdAguaEconomizadaPerCent = (qtdAguaEconomizada * 100)/qtdIrrigadoSemSolucao 
  sofar = {
      'Quantidade de dias': qtdDias, 
      'Quantidade que seria irrigado sem a solucao': round(qtdIrrigadoSemSolucao,2), 
      'Quantidade que foi irrigado': round(qtdFoiIrrigado,2),
      'Quantidade de agua economizada': str(round(qtdAguaEconomizada,2)) + " - " + str(round(qtdAguaEconomizadaPerCent,2)) + '%'
  }
  return sofar


def getData(data):
  f = open('./CATD/environment/config.txt', 'r')
  line = f.readline()
  d = json.loads(line)
  retorno = d[data]
  return retorno