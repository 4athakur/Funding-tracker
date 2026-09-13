API_K = "6i5gmMA1mPuMwsYkD5txDsshw4XYHJ"
API_S = "F40KLO5rg3SJOq6D4f3OdEdcoiZo9M9xUx53MsXse2M19xUK4Ta67JDSYp3F"
path = "/v2/funding_rates"



BASE_URL = "https://api.india.delta.exchange"
path_wallet_balance="/v2/wallet/balances"

coinddcx_api_key="cab820cb110f98e3299deeff872d5deafecc92f7f95e39a9"
coinddcx_api_secret="a7c89815abff0bb3c88386d11cd7c093ffe8945f1155e3cdb2d3075ae75412e8"
#---------------------------------------------------------------------------------------------


# Common_symbol_betweeb_CD_&_DE.py
import requests,json
#    --------------------------------------------symbole in Delta Exchange--------------------

headers = {
  'Accept': 'application/json'
}
# r = requests.get('https://api.india.delta.exchange/v2/products', params={"expiry_interval": 28800 }, headers = headers)
r = requests.get('https://api.india.delta.exchange/v2/products', headers = headers)

rr=r.json()
DE_symboll=[]
# with open('ress.json','w')as f:
#    json.dump(rr,f)
count=0
def DE_symbol():
  res=[]
  for item in rr['result']:
      global count
      count=count+1
      if item['contract_type']=="perpetual_futures":
    #  print(item['symbol'])
       res.append(item['symbol'])
      DE_symboll.append(item['symbol'])
  return res
#    -------------------------------------------------symbole in coindcx--------------------
url = "https://api.coindcx.com/exchange/v1/derivatives/futures/data/active_instruments?margin_currency_short_name[]=USDT"
r= requests.get(url)
res=r.json()
# with open('res.json','w')as f:
#    json.dump(res,f)
count2=0
for i in res:
   #  with open("data.txt",'a') as f:
   #      f.write(i+'\n')
    count2 = 1+count2

def CD_symbol():
   re=[]
   for i in res:
      re.append(i)
   return re
#--------------------------------------------------------------------------------------------
cd_symbol=CD_symbol()
de_symbol=DE_symbol()

only_de_symbol=[]
only_cdx_symbol=[]
a=[]
for i in de_symbol:
   only_de_symbol.append(i[0:-3])
c=0
for i in cd_symbol:
   if i[-5:]=='_USDT':
     only_cdx_symbol.append(i[2:-5])
     c=c+1

#---------------------------------------total common items--------------------------------------------
def common_items(list1, list2):
    a=[]
    for i in list1:
       if i in list2:
           a.append(i) 
    return a
#----------------list which contain only common symbol between Delta Exchange and CoinDcx---
a=common_items(only_de_symbol,only_cdx_symbol)
def absolute_common_items():
   return a
#-------------------------------------------------------printing not common items---------------
ss=0
for i in only_de_symbol:
   if i not in a:
    ss=ss+1
   #  print(i , "is not common")
print(ss," are not common items")
#-----------------------------------------------printing some useful information---------------
print("Total common items are",len(a)," on CDX and DE exchanges")

# print("Total future perpetula coin listed at Delta Exchange are : ",len(only_cdx_symbol))
# print("Total future perpetula coin listed at Delta Exchange are : ",len(only_de_symbol))
#--------------------------------------------------------------------------------------------
  