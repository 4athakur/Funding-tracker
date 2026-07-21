import asyncio,requests,time

url='https://api.india.delta.exchange/v2/products/AIOUSD'

def data():
    head = {'Accept': 'application/json'}
    re=requests.get(url,params={},headers=head)
    data=re.json()
    print(data)

start_time = time.time() 
data()
end_time=time.time()

print("Total fetch time is :",end_time-start_time)

