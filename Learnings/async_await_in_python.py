import asyncio,requests,time,aiohttp

url='https://api.india.delta.exchange/v2/products/AIOUSD'
url2='https://public.coindcx.com/market_data/orderbook?pair=BTCUSDT'

async def n():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print(response.status)
            s=time.time()
            data= await response.json()
            e=time.time()
            print(data)
            print("fetching time ",e-s)

async def cdcx():
    async with aiohttp.ClientSession() as session:
        async with session.get(url2) as response:
            s=time.time()
            data=await response.json()
            e=time.time()
            print(data)
            print("fetching time ",e-s)

async def neww():
    async with aiohttp.ClientSession() as session:
        async with session.get(url2) as response:
            s=time.time()
            data= await response.json()
            e=time.time()
            print("fetching time is: ",e-s)

async def mm():
   l= await asyncio.gather(n(),cdcx())
asyncio.run(mm())

async def data():
    head = {'Accept': 'application/json'}
    re=requests.get(url,params={},headers=head)
    data=re.json()
    # print(data)

start_time = time.time() 
asyncio.run(data())
end_time=time.time()
print("Total fetch time is without aiohttp: ",end_time-start_time)
#--------------------------------------------------------------------------
# async def t1():
#     print("first task")
#     await asyncio.sleep(3)
#     print('first task finished')
#     return 1

# async def t2():
#     print("second task")
#     await asyncio.sleep(0)
#     raise ValueError("aaya na error")
#     print('second task finished')


# async def main():
#    r= await asyncio.gather(t1(),t2(),return_exceptions=True)
#    print("result", r)

# asyncio.run(main())