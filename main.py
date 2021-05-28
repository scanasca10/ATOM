import pandas as pd
import json
import requests
import datetime
import calendar

coin = requests.get('https://api.coincap.io/v2/assets?limit=30') #limit 30 because coins are ranked already
coin=json.loads(coin.text)
coins_df = pd.json_normalize(coin['data'])

currentdate = datetime.datetime.utcnow()

current_year = currentdate.year

endDate = datetime.datetime.timestamp(currentdate)*1000

start_datetime = datetime.datetime(current_year, 1, 1, 0, 0, 0, 1)

startDate = datetime.datetime.timestamp(start_datetime)*1000
assets = list()

for coinId in coins_df.id:
    url = "https://api.coincap.io/v2/assets/" + coinId + "/history?interval=d1&start=" + str(startDate) + "&end=" + str(endDate)
    endpoint = requests.get(url)
    data=json.loads(endpoint.text)
    result={'id': coinId, 'history': data['data']}
    assets.append(result)

df_assets = pd.DataFrame(assets)
ratesPerDay = list()
for asset in assets:
    coinHistory = asset['history']
    coinId = asset['id']
    for day in coinHistory:  
        a = {'date': day['date'], 'coin':coinId, 'rateUsd': day['priceUsd']}
        ratesPerDay.append(a)
rates_df = pd.DataFrame(ratesPerDay)

euro = requests.get('https://api.coincap.io/v2/rates/euro') #Only last day exchange rate is available so it cant be calculated DOD
euro=json.loads(euro.text)
euro_df = pd.json_normalize(euro['data'])
euro_rate = euro_df['rateUsd'].max()

for row in rates_df:
   rates_df['rate_usd_to_eur'] = euro_rate

print(rates_df)

rates_df.to_csv("ninetynine_rates.csv")
