import requests,json
import pandas as pd
#-------------------------------------------------------------------------------------------
from config import absolute_common_items
absolute_common_items=absolute_common_items()
common_exchange_symbol=['B-'+w+'_USDT' for w in absolute_common_items]
#-------------------------------------------------------------------------------------
url = "https://public.coindcx.com/market_data/v3/current_prices/futures/rt"
resp = requests.get(url)
data = resp.json()
symbol = "B-HANA_USDT"   # try this format
a=data['prices'].keys()                         #stores symbol from CDX
data_dict_from_DCX_for_fr_and_symbol={}
#----------------------------------------------data_dict_from_DCX_for_fr_and_symbol-------------------
for symbol, info in data["prices"].items():
    mp=info.get('mkt',0)
    fr = info.get("fr", 0)
    efr = info.get("efr", 0)
    efr_val = float(efr)*100
    # Format to 6 decimal places
    data_dict_from_DCX_for_fr_and_symbol.update({symbol:efr_val})
    try:
        # ensure fr is numeric
        fr_val = float(fr)*100
    except (TypeError, ValueError):
        continue
#-----------------------------------------------------------------------------------------------
with open("da.json", 'w') as f:
 json.dump(data,f) 
count=0
for i,j in data['prices'].items():
#    print(j.get('mkt',0))
   count =count+1
#---------------------------------getting funding rate data from Delta Exchange--------------------------
headers = {'Accept': 'application/json'}
r = requests.get('https://api.india.delta.exchange/v2/tickers', params={'contract_types':"perpetual_futures"}, headers = headers)
data_delta_exchange=r.json()
# with open("aaaa.json",'w')as f:
#     json.dump(data_delta_exchange,f)
c=0
data_dict_from_DE_for_fr_and_symbol={}                                                  # delta exchange data is here
for k in data_delta_exchange['result']:
   c=c+1
   sy=k['symbol']
   data_dict_from_DE_for_fr_and_symbol.update({'B-'+k['symbol'][:-3]+'_USDT':k["funding_rate"]})
    # if float(k['funding_rate']) > 0.2 or float(k['funding_rate'])< -0.2:
    #  print(k['symbol']+" fundig rate is "+ k['funding_rate'])
converted_dict = {k: float(v) for k, v in data_dict_from_DE_for_fr_and_symbol.items()}
print(f"Total items for fr status from delta exchane is: {c}")
r=list(data_dict_from_DE_for_fr_and_symbol.keys())
#--------------------------------------------------------------------------------------------------------
ii=0
iii=0
# Iterate through all symbols and print FR + EFR in readable format
for symbol, info in data["prices"].items():
    mp=info.get('mkt',0)
    fr = info.get("fr", 0)
    efr = info.get("efr", 0)
    # Format to 6 decimal places
    try:
        # ensure fr is numeric
        fr_val = float(fr)*100
        efr_val = float(efr)*100
    except (TypeError, ValueError):
        continue
    # if symbol == 'B-AIOT_USDT':                          set symbol condition filter here
    if(symbol in common_exchange_symbol and symbol in r):
     ii+=1
     percentage=.1#                                        set percentage filter here
     diff=data_dict_from_DCX_for_fr_and_symbol[symbol]-converted_dict[symbol]
     res=abs(diff)
     if res >percentage:
        iii+=1
        print(f"Arbitrage Spoted with🔥{res:0.3f}% 🔥Funding rate {symbol} on     CoinDCX -> {data_dict_from_DCX_for_fr_and_symbol[symbol]} and           Delta Exchange -> {converted_dict[symbol]}")
    #   print(f"{info.get('mkt')} {info.get('mp')} :Estimated Next Funding Rate = {fr_val:.6f}, Current Funding Rate on CDX = {efr_val:.6f}")
print(f"\nTotal Results are: {iii}")
print(ii)


