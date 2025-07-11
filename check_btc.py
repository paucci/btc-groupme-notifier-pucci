import requests
import os

GROUPME_BOT_ID = os.environ.get("GROUPME_BOT_ID")
ATH_FILE = "last_ath.txt"
MIN_INCREMENT = 100  # Notify only if price is at least $100 higher than last ATH

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
        return 117000  # Starting fallback ATH

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

    if current_price >= last_ath + MIN_INCREMENT:
        post_to_groupme(f"GENTLEMEN! It is my pleasure to inform you - 🚀 New Bitcoin all-time high! 🎉 Price: ${current_price:,.2f} (previous ATH: ${last_ath:,.2f})")
        write_new_ath(current_price)
    else:
        print(f"BTC price ${current_price:,.2f} has not increased by ${MIN_INCREMENT} over last ATH ${last_ath:,.2f}")

if __name__ == "__main__":
    main()
