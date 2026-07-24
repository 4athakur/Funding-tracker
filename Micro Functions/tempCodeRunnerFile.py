import requests
def DE_fr_for_a_symbol(symbol_name):
    headers = {'Accept': 'application/json'}
    r = requests.get('https://api.india.delta.exchange/v2/tickers', params={'contract_types':"perpetual_futures"}, headers = headers)
    data_delta_exchange=r.json()
    for i in data_delta_exchange['result']:
        if i['symbol']== symbol_name:
            print(f"{symbol_name } Current Funding rate is: {i['funding_rate']}")
DE_fr_for_a_symbol('AIOTUSD')