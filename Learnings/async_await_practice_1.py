import asyncio,socketio,json,time,websocket

flag_for_CDX_function=1                                         # global flag_for_CDX_function
rtd_from_CDX=None
rtd_from_DE=None

async def l2_data_DE(order_type_DE):
    global flag_for_CDX_function
    input=order_type_DE
    if input.lower()=='sell':
            flag_for_CDX_function=1
    else:
            flag_for_CDX_function=0
    url='wss://public-socket.india.delta.exchange/'
    def on_open(ws):
        subscription_Msg={
        "type": "subscribe",
        "payload": {
            "channels": [
                {
                    "name": "ob_l2",
                    "symbols": [
                        "SKLUSD"                                   # Enter here your symbol
                    ]
                }
            ]
        }
    }   
        print("Connection Established! ")
        ws.send(json.dumps(subscription_Msg))

    def on_msg(ws, message):
        global rtd_from_DE
        count=0
        latency=None
        i=time.time()
        # msg=message
        e=time.time()
        latency=(e-i)*1000000000    
        data=json.loads(message)
        if input.lower()=="buy":
         print("Minimum Buying at DE: ",data['b'][0], count, f"latency = {latency:.3f}","ms")
         rtd_from_DE=data['b'][0]

        if input.lower()=="sell":
         print("Maximum Selling Price: ",data['a'][0], count, f"latency = {latency:.3f}","ms")
         rtd_from_DE=data['b'][0]     
        count+=1
    def on_close(ws,status_code,close_msg):
        print("Connection Closed")
    ws= websocket.WebSocketApp(url,
                            on_open=on_open,
                            on_message=on_msg,
                            on_close=on_close
                            )
    ws.run_forever() 

#-------------------------------------------------------CDX server------------------------------------------------------
async def l2_data_CDX():
    sio=socketio.Client()
    @sio.on('depth-update')
    def on_update(data):
        global rtd_from_CDX
            # Parse the inner JSON string into a dict
        parsed_data = json.loads(data['data'])
        info = {
            "data": parsed_data
        }                                                           
        if flag_for_CDX_function==1:
         bids= list(float(i) for i in info['data']['bids'])
         if len(bids):
          rtd_from_CDX=bids[0]
          print("latst buy is: ",bids[0])
          print(rtd_from_CDX)
        if flag_for_CDX_function==0:
         asks=list(float(k) for k in info['data']['asks'])
         if len(asks):
          rtd_from_CDX=asks[0]
          print('\tlatest selling is: ',asks[0])
          print(rtd_from_CDX)
    sio.connect("wss://stream.coindcx.com", transports=['websocket'])
    sio.emit('join', {'channelName': 'B-SKL_USDT@orderbook@10'})               # Subscribe to BTC/USDT orderbook with depth 20
    sio.wait()
#___________________________________________Exchange Order Execution Commoand center_______________________________




#________________________________________________Code Running center________________________________________


async def main():
    await asyncio.gather(l2_data_CDX(),l2_data_DE('sell'))
asyncio.run(main())
