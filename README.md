
# 🚀 BTC GroupMe Notifier

This is a simple GitHub Actions bot that checks Bitcoin price every minute, and sends a GroupMe message if Bitcoin hits a new all-time high.

- 💰 Uses CoinGecko API (free)
- 💬 Posts to your GroupMe group via a bot
- 💻 Runs entirely on GitHub Actions, so your computer can be off
- ⚡ Stores last ATH in `last_ath.txt` via GitHub cache

---

## ✅ How to use

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/btc-groupme-notifier.git
   cd btc-groupme-notifier
