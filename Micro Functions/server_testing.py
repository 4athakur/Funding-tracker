import threading
import socketio
import json
import time
import websocket

symbol='1000SATS'
ORDER_TYPE='SELL'
flag_for_CDX_function = 1
rtd_from_CDX = None
rtd_from_DE = None

# ----------------------------------------------------------------- Delta Exchange ----------------
def l2_data_DE(order_type_DE):
    global rtd_from_CDX
    global rtd_from_DE, flag_for_CDX_function
    input_val = order_type_DE
    if input_val.lower() == 'sell':
        flag_for_CDX_function = 1
    else:
        flag_for_CDX_function = 0

    url = 'wss://public-socket.india.delta.exchange/'

    def on_open(ws):
        global symbol
        subscription_msg = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {"name": "ob_l2", "symbols": [f"{symbol}USD"]}
                ]
            }
        }
        print("DE Connection Established!")
        ws.send(json.dumps(subscription_msg))

    def on_msg(ws, message):
        global rtd_from_DE
        i = time.time()
        data = json.loads(message)
        e = time.time()
        latency = (e - i) * 1000

        if input_val.lower() == "buy":
            print("Minimum Buying at DE:", data['b'][0], f"latency={latency:.3f} ms")
            rtd_from_DE = data['b'][0][0]

        if input_val.lower() == "sell":
            print("Maximum Selling Price at DE:", data['a'][0], f"latency={latency:.3f} ms")
            rtd_from_DE = data['a'][0][0]
        slippage_diff()

    def on_close(ws, status_code, close_msg):
        print("DE Connection Closed")

    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_msg,
        on_close=on_close
    )
    ws.run_forever()


# ----------------------------------------------------------------CoinDCX ----------------
def l2_data_CDX():
    global rtd_from_CDX,symbol
    sio = socketio.Client()
    @sio.on('depth-update')
    def on_update(data):
            global rtd_from_CDX
                # Parse the inner JSON string into a dict
            parsed_data = json.loads(data['data'])
            with open('DE_dataaaaaaaaaaa.json','a') as f:
               json.dump(parsed_data,f,indent=4)
            info = {
                "data": parsed_data
            }                                                           
            if flag_for_CDX_function==1:
             bids= list(float(i) for i in parsed_data['bids'])
             if len(bids):
              rtd_from_CDX=bids[0]
              print("🔥🔥🔥🔥latst buy is: ",bids[0])
              print(format(rtd_from_CDX,'.10f'))
            if flag_for_CDX_function==0:
             asks=list(float(k) for k in parsed_data['asks'])
             if len(asks):
              rtd_from_CDX=asks[0]
              print('\t🔥🔥🔥🔥latest selling is: ',asks[0])
              print(format(rtd_from_CDX,'.10f'))
    sio.connect("wss://stream.coindcx.com", transports=['websocket'])
    sio.emit('join', {'channelName': f'B-{symbol}_USDT@orderbook@10'})               # Subscribe to BTC/USDT orderbook with depth 20
    sio.wait()
                # print("🔥🔥🔥🔥Latest buy at CDX:", bids[0])
#-------------------------------------------------------------------------SLIPPAGE DIFFERENCES---------------------------------
# rtd_from_DE_list=rtd_from_DE[0]
def slippage_diff():
   if flag_for_CDX_function==1:
        print(f"\t\t\t\t\t\t\t\t\t\t\t\tDE is selling at:  {rtd_from_DE}")
        print(f"\t\t\t\t\t\t\t\t\t\t\t\tCDX is buying at:  {rtd_from_CDX}")
        if float(rtd_from_DE)>=rtd_from_CDX: 
           print("\t\t\t\t\t\t\t\t\t\t\t\tPosition opened😁😁")
   else:
        print(f"\t\t\t\t\t\t\t\t\t\t\t\tDE is buying at :  {rtd_from_DE}")
        print(f"\t\t\t\t\t\t\t\t\t\t\t\tCDX is selling at:  {rtd_from_CDX}")
        if float(rtd_from_DE)<=rtd_from_CDX: 
                    print("\t\t\t\t\t\t\t\t\t\t\t\tPosition closed")
       
# ---------------- Run both threads ----------------
if __name__=="__main__":
    T2=threading.Thread(target=l2_data_DE,args=(ORDER_TYPE,),daemon=False)
    T1=threading.Thread(target=l2_data_CDX,daemon=False)
    T1.start()
    T2.start()

    #keep thread alive
    T1.join()
    T2.join()



