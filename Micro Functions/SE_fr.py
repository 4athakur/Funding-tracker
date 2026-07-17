import requests

BASE_URL = "https://api.sharkexchange.com/v1/futures"

def get_all_futures():
    """Fetch all listed futures contracts."""
    url = f"{BASE_URL}/exchangeInfo"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["symbols"]

def get_funding_rate(symbol):
    """Fetch real-time funding rate for a given futures symbol."""
    url = f"{BASE_URL}/fundingRate?symbol={symbol}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def main():
    # Step 1: Get all listed futures contracts
    futures = get_all_futures()
    print(f"Total futures contracts: {len(futures)}\n")

    # Step 2: Loop through each contract and fetch funding rate
    for f in futures:
        symbol = f["symbol"]
        funding_data = get_funding_rate(symbol)
        print(f"Symbol: {symbol}")
        print(f"  Current Funding Rate: {funding_data['fundingRate']}")
        print(f"  Next Funding Time: {funding_data['nextFundingTime']}")
        print(f"  Mark Price: {funding_data['markPrice']}\n")

if __name__ == "__main__":
    main()
