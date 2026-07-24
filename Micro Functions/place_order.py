import requests,time


#----------------------------------------------------------------------------------
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'api-key': '****',
  'signature': '****',
  'timestamp': '****'
}

r = requests.post('https://api.india.delta.exchange/v2/orders', params={

}, headers = headers)

print(r.json())

#----------------------------------------------------------------
# python code to generate signature

timestamp = str(int(time.time()))
signature_data = method + timestamp + path + query_string + payload
signature = generate_signature(api_secret, signature_data)