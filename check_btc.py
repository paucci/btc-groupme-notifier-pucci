import requests
import os

GROUPME_BOT_ID = os.environ.get("GROUPME_BOT_ID")
ATH_FILE = "last_ath.txt"

def get_bitcoin_price_usd():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

def read_last_ath():
    try:
        with open(ATH_FILE, 'r') as f:
            return float(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 118600  # Starting fallback ATH, adjust if you like

def write_new_ath(value):
    with open(ATH_FILE, 'w') as f:
        f.write(f"{value}")

def post_to_groupme(message):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {
        "bot_id": GROUPME_BOT_ID,
        "text": message
    }
    requests.post(url, json=payload)

def main():
    current_price = get_bitcoin_price_usd()
    last_ath = read_last_ath()

    if current_price > last_ath:
        post_to_groupme(f"🚀 New Bitcoin all-time high! 🎉 Price: ${current_price:,.2f} (old ATH was ${last_ath:,.2f})")
        write_new_ath(current_price)
    else:
        print(f"BTC ${current_price:,.2f} is below ATH ${last_ath:,.2f}")

if __name__ == "__main__":
    main()
