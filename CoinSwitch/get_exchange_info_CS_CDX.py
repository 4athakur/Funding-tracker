import credentials,json
import time
import urllib.parse
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
#-------------------------------------------------------------------------------------------
from config import absolute_common_items
absolute_common_items=absolute_common_items()
common_exchange_symbol=['B-'+w+'_USDT' for w in absolute_common_items]

#----------------------------Extracting FR from CDX-------------------------------------------

# with open('info.json' , 'w') as f:
#     json.dump(data,f,indent=4)
def getting_fr_from_CDX_for_a_symbol(symbol):
    url = "https://public.coindcx.com/market_data/v3/current_prices/futures/rt"
    resp = requests.get(url)
    data = resp.json()
    # print(data['prices'])
    if symbol in data['prices']:
        fr = float(data['prices'][symbol]['efr']) * 100
        return fr
    else:
        print(f"{symbol} not found in CDX data")
        return None
#-------------------------------------------------------------------------------------

BASE_URL='https://api-trading.coinswitch.co'
API_KEY    = f"{credentials.api_key}"     # hex
SECRET_KEY = f"{credentials.secret_key}"  # hex

BASE_URL = "https://coinswitch.co"
def sign_request(method, path, params=None):
    """
    Build the headers and final URL path for an authenticated CoinSwitch
    request. Pass the returned dict as `headers=` and the returned `path`
    as the URL (after BASE_URL).

    method  — "GET" / "POST" / "DELETE"
    path    — endpoint path, e.g. "/trade/api/v2/order"
    params  — query parameters dict (for GET requests with filters)
    """
    method = method.upper()

    if params:
        sep = "&" if "?" in path else "?"
        path = path + sep + urllib.parse.urlencode(params)
    decoded_path = urllib.parse.unquote_plus(path)

    epoch = str(int(time.time() * 1000))
    message = method + decoded_path + epoch

    secret = ed25519.Ed25519PrivateKey.from_private_bytes(bytes.fromhex(SECRET_KEY))
    signature = secret.sign(message.encode("utf-8")).hex()

    headers = {
        "Content-Type": "application/json",
        "X-AUTH-APIKEY": API_KEY,
        "X-AUTH-SIGNATURE": signature,
        "X-AUTH-EPOCH": epoch,
    }
    return headers, decoded_path

def Get_Wallet_Balance():
    # Rate Limit: 	20 requests per 60 seconds
    headers, path = sign_request("GET", "/trade/api/v2/futures/wallet_balance")
    response = requests.get(BASE_URL + path, headers=headers)
    print(response.json())

Get_Wallet_Balance()
headers, path = sign_request("GET", "/trade/api/v2/futures/all-pairs/ticker",
                             params={"exchange": "EXCHANGE_2"})
response = requests.get(BASE_URL + path, headers=headers)
data=response.json()
with open('exchange_info.json','w')as f:
    json.dump(data,f,indent=4)
li=list(data['data'].keys())
print(f"\nTotal listed Future Contracts on CoinSwitch are: {len(li)}")

def cal_common_symbol_between_DE_CDX_CS():
    count=0
    LI=[]
    for i in li:
        string=i[:-4]
        if string in absolute_common_items:
            count=count+1
            # print(i," ",i[:-4], count)
            LI.append(i[:-4])
    print("Total common symbol between CDX , DE, CS are ",count)
    return LI

common_symbol_CDX_DE_CS=cal_common_symbol_between_DE_CDX_CS()
#----------------------------Extracting FR from CS-------------------------------------------
count=0
for i in li:  
    fr=float(data['data'][f'{i}']['funding_rate'])*100
    if (True): # add condition here to fast the scanning process
     count=count+1
     print(count)
     cdx = getting_fr_from_CDX_for_a_symbol("B-"+i[:-4]+"_USDT") or 0
     diff=abs(fr-cdx)
    #  print(f"\n{i} Funding Rate is: {fr:.5f} at CDX= {cdx }")
     if diff>0.3:                                                # filtering adujustment for CDX and CS
         print(f"\n{i} Funding Rate is: {fr:.5f} at CDX= {cdx }")
         print(f"Arbitrage Found 😃{diff}")
     if i[:-4] in common_symbol_CDX_DE_CS:
         print(f" \t\t\t\t{"B-"+i[:-4]+"_USDT"} Available at CDX {getting_fr_from_CDX_for_a_symbol("B-"+i[:-4]+"_USDT")}, DE AS WELL")
#--------------------------------------------------------------------------------------------
def getting_fr_from_CS_for_a_symbol(symbol):
     fr=float(symbol['data'][f'{i}']['funding_rate'])*100
     return fr