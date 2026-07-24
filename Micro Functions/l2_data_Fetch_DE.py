import websocket
import json
import time

count=1
latency=0
url='wss://public-socket.india.delta.exchange/'
# url='wss://socket-ind.testnet.deltaex.org/'
def on_open(ws):
    subscription_Msg={
    "type": "subscribe",
    "payload": {
        "channels": [
            {
                "name": "ob_l2",
                "symbols": [
                    "AIOTUSD"
                ]
            }
        ]
    }
}
           
    print("Connection Established! ")
    ws.send(json.dumps(subscription_Msg))

def on_msg(ws, message):
    global count
    global latency
    i=time.time()
    msg=message
    e=time.time()
    latency=(e-i)*1000000000
    data=json.loads(message)
    print("Maximum Selling Price: ",data['a'][0]," ","Minimum Buying at DE: ",data['b'][0], count, f"latency = {latency:.3f}","ms")
    count+=1
    with open('l2.json','a') as f:
        json.dump(data,f,indent=4)

def on_close(ws,status_code,close_msg):
    print("Connection Closed")

ws= websocket.WebSocketApp(url,
                           on_open=on_open,
                           on_message=on_msg,
                           on_close=on_close
                           )
ws.run_forever()


