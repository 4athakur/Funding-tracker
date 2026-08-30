import requests,json
def get_exchange_info():
  base_url='https://api.sharkexchange.in/'
  # Construct the URL
  full_url = f"{base_url}/v1/exchange/exchangeInfo"
  r=requests.get(full_url)
  data=r.json()
  print(r.json())
  #saving data in a json file format
  with open('daaa.json','w+') as f:
    json.dump(data,f,indent=4)
  

get_exchange_info()