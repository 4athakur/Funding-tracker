# import requests
# from pydantic import BaseModel
# def DE_fr_for_a_symbol(symbol_name: str):
#     headers = {'Accept': 'application/json'}
#     r = requests.get('https://api.india.delta.exchange/v2/tickers', params={'contract_types':"perpetual_futures"}, headers = headers)
#     data_delta_exchange=r.json()
#     for i in data_delta_exchange['result']:
#         if i['symbol']== symbol_name:
#             print(f"{symbol_name } Current Funding rate is: {i['funding_rate']}")
#             res=float(i['funding_rate'])
#     return res
# # A=DE_fr_for_a_symbol("AIOTUSD")


from pydantic import BaseModel


class test:
    # data='data'
    def __init__(self,name,age):
        self.name='lucky'
        self.age=age

    def hello(self):
        print(self)
        print("hi laku")

class student(BaseModel):
    name: str
    age: int

obj=test('amit',34)
obj.hello()
print(obj.name)

class animal:
    name='aaa'

class car(animal):
    age=34
data=car()
print(data.age)