import requests,json,time,asyncio

async def l2_price_from_delta_exchange(symbol):
    headers = {'Accept': 'application/json'}
    r = requests.get(f'https://api.india.delta.exchange/v2/l2orderbook/{symbol}', params={}, headers = headers)
    # print(r.json())
    data=r.json()
    with open('dd_delta.json','w')as f:
        json.dump(data,f,indent=4)
    print('Delta Exchange Ask is: ',data['result']['sell'][0]['price'], " and bid is ",data['result']['buy'][0]['price'])
    asyncio.sleep(3)
    return r.json()

async def l2_price_from_coindcx(symbol):
    r=requests.get(f'https://public.coindcx.com/market_data/v3/orderbook/{symbol}-futures/50')
    data=r.json()
    with open('dd_coindcx.json','w')as f:
        json.dump(data,f,indent=4)
    print('COINDCX Ask is: ',data['asks'], " and bid is ",data['bids'])
    asyncio.sleep(3)
    return r.json()

# async def main():
#     # data1=l2_price_from_delta_exchange('SKLUSD')
#     # data2=l2_price_from_coindcx('B-SKL_USDT')
#     await asyncio.gather(l2_price_from_delta_exchange('SKLUSD'),l2_price_from_coindcx('B-SKL_USDT'))
#     # print(data1)
#     # print(data2)
# asyncio.run(main())

data = await l2_price_from_coindcx('HANUSD')
# async def task():
#     print("start")
#     await asyncio.sleep(1)
#     print("end")

# async def game():
#     print("playing game")
#     await asyncio.sleep(3)
#     # time.sleep(2)
#     print("kheel bedha game")

# async def main():
#     await asyncio.gather(task(),game())
# asyncio.run(main())
