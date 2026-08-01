import requests

def sms_alert(network_address):
    # server = "http://10.105.178.144:8080/send-sms"
    server=f"http://"+network_address+":8080/send-sms"
    headers = {
        "X-API-Key": "gw_29a60e72cfc442f5ad95",
        "Content-Type": "application/json"
    }
    payload = {
        "phone_number": ["+919015353925","+918295647631","+919713393563"],#   "+919713393563","+919548271418","+919812553075",
        "message": "PAUCH GAYA ?",
        "sim_slot": 0
    }

    response = requests.post(server, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
#______________________________________________________________________________________________________________\
sms_alert("10.123.137.54")
