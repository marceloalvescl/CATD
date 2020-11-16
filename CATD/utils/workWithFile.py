import json
from datetime import datetime


def writeIntoFile(d):
  f = open('../static/requisicoes.txt', 'a')
  j = json.dumps(d)
  f.write(j)
  f.write("\n")
  f.close()

def getLastRequestDate():
  f = open('../static/requisicoes.txt', 'r')
  lastline = f.read().splitlines()[-1]
  d = json.loads(lastline)
  data = d['Data']
  horario = d['Horario']
  return data, horario

def compareLastDateAndHour(data, horario):
  now = datetime.now()
  dataAtual = now.strftime("%d/%m/%Y")
  horarioAtual = now.strftime("%H:%M:%S")

  data = datetime.strptime(data.strip(), "%d/%m/%Y")
  horario = datetime.strptime(horario.strip(), "%H:%M:%S")

  dataAtual = datetime.strptime(dataAtual.strip(), "%d/%m/%Y")
  horarioAtual = datetime.strptime(horarioAtual.strip(), "%H:%M:%S")

  if(data < dataAtual):
    if(horario < horarioAtual):
      return True
  print("Ainda não está no horário para requisição")
  return False

def getData(data):
  f = open('./environment/config.txt', 'r')
  line = f.readline()
  d = json.loads(line)
  retorno = d[data]
  return retorno
