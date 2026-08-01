aa={"amit":"thakur","roll":1}
print(aa['amit'])

new= {
       "data": {
        "ts": 1785158821276,
        "vs": 54101024,
        "asks": {},
        "bids": {
            "0.00382": "487732",
            "0.00378": "706163",
            "0.00377": "440488"
        },
        "type": "depth-update",
        "pts": 1785158821276,
        "E": 1785158821205,
        "pr": "spot",
        "s": "SKLUSDT"
    }
}
print(bool(new['data']['bids']))
# bids=list([float(i) for i in new['data']['bids']])
# print(type(bids))
# print(bids)
# print(type(bids[0]))