import requests
from config import absolute_common_items
count=0
#____(PHASE 1)__________________________________ getting common coins list first between DE and CDX_____________
absolute_common_items=absolute_common_items()
common_exchange_symbol_for_CDX=['B-'+w+'_USDT' for w in absolute_common_items] #CDX list of common coins
#_____________________________________________________
def common_symbol_for_DE(pass_common_symbol_list):
    curating_symbol_for_DE=[]
    store=pass_common_symbol_list
    for i in store:
        curating_symbol_for_DE.append(i[2:-5]+'USD')
    return curating_symbol_for_DE
DE=common_symbol_for_DE(common_exchange_symbol_for_CDX)
#____(PHASE 2)__________________Fetching orderbook data from CDX for particular common symbol___________________
def fetch_l2_data_from_DE(symbol):
    headers = {'Accept': 'application/json'}
    r = requests.get(f'https://api.india.delta.exchange/v2/l2orderbook/{symbol}', params={}, headers = headers)
    data=r.json()
    bid=float(data['result']['buy'][0]['price'])
    ask=float(data['result']['sell'][0]['price'])
    ###################################################
    # if(abs(((bid-ask)/bid)*100)>= 0.5):
    #     print('from outside')
    #     print("🔥🔥🔥🔥🔥big spread identified",((bid-ask)/bid)*100)
    #     print(f'buy is : {bid} , sell is {ask} at DE for {symbol} spread is {((bid-ask)/bid)*100}\n')
    #################################################
    return bid,ask,symbol

def fetch_l2_data_from_CDX(symbol):
    endpoint = f"https://public.coindcx.com/market_data/v3/orderbook/{symbol}-futures/10"
    r=requests.get(endpoint)
    data=r.json()
    bids=[float(key) for key in data['bids'].keys()]
    asks=[float(keys) for keys in data['asks'].keys()]
    # print(f'for {symbol} bid is : {bids[0]} and ask is: {asks[0]}\n')
    return bids[0],asks[0],symbol
#____(PHASE 3)_________________________Spreadcalculation______________________________________
for i in common_exchange_symbol_for_CDX:
    res_cdx=fetch_l2_data_from_CDX(i) # res_cdx[0] ==buying price at cdx , res_cdx[1] ==selling price at CDX same for DE
    res_de=fetch_l2_data_from_DE(i[2:-5]+'USD')
    count =count+1
    print(count)
    # ------------------calculating spread percentage---------------------
    if ((abs((res_de[0]-res_cdx[1])/res_de[0])*100)>=0.3):
            res=(abs((res_de[0]-res_cdx[1])/res_de[0])*100)
            if(res_de[1]<res_cdx[1]):
                print(f"{i} provide HUGE SPREAD of: {((res_de[0]-res_cdx[1])/res_de[0])*100}% 🔥🔥🔥🙌{res_de} buy DE at {res_de[0]} and sell CDX at {res_cdx[1]} ")
            if(res_de[0]>res_cdx[0]):
                ress=((res_de[1]-res_cdx[0])/res_de[1])*100
                print(f"{i} provide HUGE SPREAD of: {ress}% 🔥🔥🔥🙌{res_cdx[0]} sell DE at {res_de[1]} and buy CDX at {res_cdx[0]} ")

print("Programm end !")
# #______________________________________________________________________________________________________
# print(fetch_l2_data_from_CDX('B-ARIA_USDT'))
# print(fetch_l2_data_from_DE('ARIAUSD'))

# for i in DE:
#     print(fetch_l2_data_from_DE(i))


