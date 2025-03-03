import requests
import json
import datetime
import os
import pytz

def main():  
  try:
    discordUrl = os.environ["DISCORDWINDWEBHOOK"]
  except KeyError:
      raise Exception("Discord webhook not available!")

  windDegreeMax = 315
  windDegreeMin = 225
  windSpeedMin = 5

  apiKey = "3f4a54aaa3ce4097ae6185031250203"
  location = "39.04456,-84.67229"
  forecastDays = 1
  airQualityInfo = "no"
  weatherAlerts = "no"
  url = "https://api.weatherapi.com/v1/forecast.json?key={}&q={}&days={}&aqi={}&alerts={}".format(apiKey, location, forecastDays,airQualityInfo,weatherAlerts)

  res = requests.get(url)
  data = json.loads(res.text)

  forecastArray = []

  eastern_tz = pytz.timezone('US/Eastern')
  utc_tz = pytz.timezone('UTC')

  for i in data["forecast"]["forecastday"]:
     for j in i["hour"]:
        datetimeObject = datetime.datetime.fromtimestamp(j["time_epoch"])
        datetime_utc = utc_tz.localize(datetimeObject)
        datetime_eastern = datetime_utc.astimezone(eastern_tz)
        friendlyTime = datetime_eastern.strftime("%I:%M%p")
        
        if (j["wind_degree"] < windDegreeMax and j["wind_degree"] > windDegreeMin) and (j["wind_mph"] > windSpeedMin):
          forecastArray.append({"name": friendlyTime,"value": "💨 Conditions favorable for RWY 27 arrivals.\n Wind: {} mph\n Gust: {} mph\n Direction: {} ".format(j["wind_mph"],j["gust_mph"],j["wind_dir"]),"inline":"true"})
        else:
          forecastArray.append({"name": friendlyTime,"value": "Wind: {} mph\nGust: {} mph\nDirection: {} ".format(j["wind_mph"],j["gust_mph"],j["wind_dir"]),"inline":"true"})

  now = datetime.datetime.now()
  now_utc = utc_tz.localize(now)
  now_eastern = now_utc.astimezone(eastern_tz)
  formatted_time = now_eastern.strftime("%Y-%m-%d")

  discordHeaders = {"Content-Type":"application/json"}
  discordData = json.dumps ({"embeds": [{"title": formatted_time,"fields": forecastArray}]})
  r = requests.post(discordUrl, headers = discordHeaders, data = discordData)

  if r.status_code != 204:
    raise Exception(r)

if __name__ == '__main__':
    main()