from datetime import datetime
import json
import time
import requests

def getInformacoes():
  try:
    response = requests.get('http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/8173/days/15?token=61e58793d4fef044dddb3f86f078ee8a')
    date, horario, rainProbability, precipitationAmount = getRainInfoFromJson(response.json())
    response = {
      "Data": date,
      "Horario": horario,
      "Probabilidade de chuva": str(rainProbability) + "%",
      "Precipitacao de chuva": str(precipitationAmount) + "mm"
    }
    writeIntoFile(response)
  except Exception as e:
    print(e)
  return response

def getRainInfoFromJson(json):
  date = json['data'][0]['date_br']
  now = datetime.now()
  horario = now.strftime("%H:%M:%S")
  rainProbability = json['data'][0]['rain']['probability']
  precipitationAmount = json['data'][0]['rain']['precipitation']
  return date, horario, rainProbability, precipitationAmount

def writeIntoFile(d):
  f = open('./static/requisicoes.txt', 'a')
  j = json.dumps(d)
  f.write(j)
  f.write("\n")
  f.close()

def getLastRequestDate():
  f = open('./static/requisicoes.txt', 'r')
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
  dataAtual = datetime.strptime(dataAtual.strip(), "%d/%m/%Y")
  horario = datetime.strptime(horario.strip(), "%H:%M:%S")
  horarioAtual = datetime.strptime(horarioAtual.strip(), "%H:%M:%S")
  if(data < dataAtual):
    if(horario < horarioAtual):
      return True
    else:
      print("Ainda não está no horário para requisição")
  else:
    print("Ainda não está no horário para requisição")
  return False


while(True):
  data, horario = getLastRequestDate()
  print(data)
  print(horario)
  if(compareLastDateAndHour(data, horario)):
    getInformacoes()
  time.sleep(3600)
