import requests,json,time
from config import absolute_common_items
symbols=absolute_common_items()

#------------------------------Fetching l2 order details from Delta Exchange-------------------
while 1:
 for i in symbols:
  headers = { 'Accept': 'application/json'}
  r = requests.get(f'https://api.india.delta.exchange/v2/l2orderbook/{i+'USD'}', params={'depth':1
  }, headers = headers)
  data=r.json()
#   print(data)
  with open("d.json",'a+') as f:
    json.dump(data,f,indent=4)
  print(i,"Price is: ", data['result']['sell'][0]['price'])
time.sleep(30)
