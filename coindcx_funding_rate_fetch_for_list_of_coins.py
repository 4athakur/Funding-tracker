import socketio


symbol='HANAUSD'
url = "wss://stream.coindcx.com"
obj=socketio.Client()
# print(type(obj))

@obj.event
def connect():
    print("connection established")


@obj.event
def disconnect():
    print("Connection Revoked")

obj.connect(url, transports = 'websocket')


obj.emit('join', {'channelName':"currentPrices@futures@rt"})#asking for data

# Subscribe to funding rate channels for multiple symbols
# symbols = ['BTCUSD']
# for sym in symbols:
#     obj.emit('join', {'channelName': f'funding-rate:{sym}'})


@obj.on('currentPrices@futures#update')
def on_message(response):
  print(response["data"])
  print("\n")
# obj.on('currentPrices@futures#update')
# print(dir(obj))
obj.wait()
obj.disconnect()