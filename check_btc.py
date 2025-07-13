import os
import requests

ATH_FILE = "last_ath.txt"
INITIAL_ATH = 119265  # or set to 0 if you want

GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")

def get_current_btc_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["bpi"]["USD"]["rate"].replace(",", ""))
    except Exception as e:
        print(f"⚠️ Error fetching BTC price: {e}")
        return None

def notify_groupme(message):
    if not GROUPME_BOT_ID:
        print("⚠️ GROUPME_BOT_ID not set.")
        return
    payload = {"bot_id": GROUPME_BOT_ID, "text": message}
    try:
        response = requests.post("https://api.groupme.com/v3/bots/post", json=payload)
        if response.status_code == 202:
            print("✅ Successfully posted to GroupMe.")
        else:
            print(f"⚠️ Failed to post to GroupMe: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"⚠️ Exception posting to GroupMe: {e}")

def ensure_ath_file_exists():
    if not os.path.exists(ATH_FILE):
        with open(ATH_FILE, "w") as f:
            f.write(str(INITIAL_ATH))
        print(f"🚀 Created {ATH_FILE} with initial ATH of {INITIAL_ATH}.")

def read_last_ath():
    with open(ATH_FILE, "r") as f:
        value = float(f.read().strip())
    return value

def write_new_ath(value):
    with open(ATH_FILE, "w") as f:
        f.write(str(value))
    print(f"✍️ Updated {ATH_FILE} to {value}.")

def main():
    ensure_ath_file_exists()
    last_ath = read_last_ath()
    print(f"📈 Last recorded ATH: ${last_ath}")

    current_price = get_current_btc_price()
    if current_price is None:
        print("❌ Could not get current BTC price, exiting.")
        return

    print(f"💰 Current BTC price: ${current_price}")

    if current_price > last_ath + 100:
        message = f"🚀 New BTC ATH! Price is now ${current_price}, beating last ATH of ${last_ath}."
        notify_groupme(message)
        write_new_ath(current_price)
    else:
        print(f"ℹ️ No new ATH. Needs to beat ${last_ath + 100}.")

if __name__ == "__main__":
    main()

