import requests,json
symbol='B-ARIA_USDT'
#____(PHASE 2)_______Fetching orderbook data from CDX for particular common symbo_______
def fetch_l2_data_from_DE(symbo=symbol):
    headers = {'Accept': 'application/json'}
    r =requests.get(f'https://api.india.delta.exchange/v2/l2orderbook/{symbo[2:-5]+'USD'}', params={}, headers = headers)
    data=r.json()
    with open("result.json",'w') as f:
        json.dump(data,f,indent=4)
    bid=float(data['result']['buy'][0]['price'])
    ask=float(data['result']['sell'][0]['price'])
    return bid,ask,symbo

def fetch_l2_data_from_CDX(symbo=symbol):
    endpoint = f"https://public.coindcx.com/market_data/v3/orderbook/{symbo}-futures/10"
    r= requests.get(endpoint)
    data=r.json()
    bids=[float(key) for key in data['bids'].keys()]
    asks=[float(keys) for keys in data['asks'].keys()]
    return bids[0],asks[0],symbo


for i in range(1,1000):
    l2_de=fetch_l2_data_from_DE()
    l2_cdx=fetch_l2_data_from_CDX()
    print(i)
    if(l2_de[1]<l2_cdx[1]):
        print(f"SPREAD is: {((l2_de[0]-l2_cdx[1])/l2_de[0])*100}% 🔥 BUY DE at {l2_de[0]} and SELL CDX at {l2_cdx[1]} ")
    if(l2_de[0]>l2_cdx[0]):
        ress=((l2_de[1]-l2_cdx[0])/l2_de[1])*100
        print(f"🔥SPREAD is: {ress}%  SELL DE at {l2_de[1]} and 🔥BUY CDX at {l2_cdx[0]} ")
