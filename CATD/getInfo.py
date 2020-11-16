import sys
sys.path.append("./utils")

import time
import utils.workWithJson as wj
import utils.workWithFile as wf
import requests

def getInformacoes():
  try:
    response = requests.get('http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/8173/days/15?token=61e58793d4fef044dddb3f86f078ee8a')
    date, horario, rainProbability, precipitationAmount = wj.getRainInfoFromJson(response.json())
    amountOfWater = defineAmountOfWater(rainProbability, precipitationAmount)
    amountOfTime = defineAmountOfTime(amountOfWater)
    response = {
      "Data": date,
      "Horario": horario,
      "Probabilidade de chuva": str(rainProbability) + " %",
      "Precipitacao de chuva": str(precipitationAmount) + " mm",
      "Quantidade de agua a regar no dia": str(amountOfWater) + " litros",
      "Tempo de irrigacao no dia": str(round(amountOfTime / 60)) + " minutos"
    }
    wf.writeIntoFile(response)
  except Exception as e:
    print(e)
  return response

#qtdChuvaPrecipitada = (áreaDestinadaAoPlantio x precipitaçãoPrevista)/5800km² 
def defineAmountOfWater(rainProbability, precipitationAmount):
  if(rainProbability > 50):
    fieldSize = int(wf.getData("AreaDestinadaAoPlantioEmkm2"))
    qtdChuvaPrecipitada = (fieldSize * precipitationAmount)/5800
    amountOfWater = 3 - qtdChuvaPrecipitada
    return round(amountOfWater,2)

def defineAmountOfTime(amountOfWater):
  vazaoPorHora = int(wf.getData("VazaoPorHora"))
  amountOfTime = (3600 * amountOfWater) / vazaoPorHora
  return amountOfTime
  
while(True):
  data, horario = wf.getLastRequestDate()
  print(data)
  print(horario)
  if(wf.compareLastDateAndHour(data, horario)):
    getInformacoes()
  time.sleep(3600)
