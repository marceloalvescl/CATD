import json
from datetime import datetime


def getRainInfoFromJson(json):
  date = json['data'][0]['date_br']
  now = datetime.now()
  horario = now.strftime("%H:%M:%S")
  rainProbability = json['data'][0]['rain']['probability']
  precipitationAmount = json['data'][0]['rain']['precipitation']
  return date, horario, rainProbability, precipitationAmount