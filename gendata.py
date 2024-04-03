import requests as r
import json

APIKEY = open("APIKEY.txt","r").read()
inp = input("input stock that you'd like the bot to trade: ")
data_raw = r.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={inp}&apikey={APIKEY}').json()

json.dump(data_raw,open("data.json","w"))