import socketio,json

sio = socketio.Client()

@sio.on('depth-update')
def on_update(data):
    # Parse the inner JSON string into a dict
    parsed_data = json.loads(data['data'])
    info = {
        "data": parsed_data
    }
    with open('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json','a')as f:
        json.dump(data,f,indent=4)
    # Save properly nested JSON
    if info['data']['bids'] and info['data']['asks'] :
        bids= list(float(i) for i in info['data']['bids'])
        asks=list(float(k) for k in info['data']['asks'])
        print("latest buy is: ",bids[0],'\tlatest selling is: ',asks[0])

    # print("latst bids is: 🙌",info['data']['bids'],'\tlatest asks is: 🙌',info['data']['asks'])
sio.connect("wss://stream.coindcx.com", transports=['websocket'])
# Subscribe to BTC/USDT orderbook with depth 20
sio.emit('join', {'channelName': 'B-1000SATS_USDT@orderbook@10'})
sio.wait()
