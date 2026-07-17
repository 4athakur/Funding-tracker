import requests
import time
import base64
import hashlib
import nacl.signing

def sign_request(method, path, params=None):
    # TODO: implement request signing according to the API spec
    # for example, build a query string and compute a signature.
    headers = {"Content-Type": "application/json"}
    return headers, path

BASE_URL = "https://coinswitch.co"
headers, path = sign_request(
    "GET",
    "/trade/api/v2/futures/all-pairs/ticker",
    params={"exchange": "EXCHANGE_2"}
)
response = requests.get(BASE_URL + path, headers=headers)
print(response.json())