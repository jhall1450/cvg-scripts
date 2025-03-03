import requests
import json
import datetime
import os
import pytz

def main():

  try:
    discordUrl = os.environ["DISCORDATISWEBHOOK"]
  except KeyError:
      raise Exception("Discord webhook not available!")

  weatherUrl = "https://datis.clowd.io/api/KCVG"

  res = requests.get(weatherUrl)
  data = json.loads(res.text)

  for i in data:
    if i["type"] == "arr":
      arrivalATIS = i["datis"]
    elif i["type"] == "dep":
      departureATIS = i["datis"]

  eastern_tz = pytz.timezone('US/Eastern')
  now = datetime.datetime.now()
  now_eastern = eastern_tz.localize(now)
  formatted_time = now_eastern.strftime("%Y-%m-%d %H:%M:%S")

  discordHeaders = {"Content-Type":"application/json"}
  discordData = json.dumps ( {"embeds": [{"title": formatted_time,"fields": [{"name": "Arrivals","value": arrivalATIS},{"name": "Departures","value": departureATIS}]}]})
  r = requests.post(discordUrl, headers = discordHeaders, data = discordData)

  if r.status_code != 204:
    raise Exception(r)

if __name__ == '__main__':
  main()