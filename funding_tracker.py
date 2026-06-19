# Place new order
# method = 'GET'
# timestamp = str(int(time.time()+1))
# path = '/v2/orders'
# url = f'{base_url}{path}'
# query_string = '?product_id=1&state=open'
# payload=''
# # payload = "{\"order_type\":\"limit_order\",\"size\":3,\"side\":\"buy\",\"limit_price\":\"0.0005\",\"product_id\":16}"
# signature_data = method + timestamp + path + query_string + payload
# signature = generate_signature(api_secret, signature_data)
import hashlib
import hmac
import requests
import time
from config import *

base_url = 'https://api.india.delta.exchange'
api_key = "xWEGAYPyuSrSKn8mdvD0l0S07e31Lp"
api_secret = "r9eywOUADxTmYaC2QenesEHLMjqM3C2efGQrGAks3NWcILIktJdihrKAp0r3"
                                        #generating signature
def generate_signature(secret, message):
    message = bytes(message, 'utf-8')
    secret = bytes(secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    return hash.hexdigest()

# Get open orders
method = 'GET'
timestamp = str(int(time.time()))
path = '/v2/positions/margined'
url = f'{base_url}{path}'
query_string = '?product_id=1&state=open'
payload = ''
signature_data = method + timestamp + path + query_string + payload
signature = generate_signature(api_secret, signature_data)

headers = {
  'Accept': 'application/json',
  'api-key': api_key,
  'signature': signature,
  'timestamp': timestamp
}

# r = requests.get('https://api.india.delta.exchange/v2/positions/margined', params=query_string, headers = headers)
r = requests.get(url+query_string, headers = headers)


print(r.json())