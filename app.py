import requests
from flask import Flask, jsonify
from nba_api.stats.endpoints import playergamelogs
import os
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch fresh proxies
def get_fresh_proxies():
    url = "https://sslproxies.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []
    
    for row in soup.select("table tbody tr"):
        tds = row.find_all("td")
        proxy = f"{tds[0].text}:{tds[1].text}"
        proxies.append(proxy)
    
    return proxies

# Function to make requests using rotating proxies
def fetch_with_proxy(url):
    proxies = get_fresh_proxies()
    random.shuffle(proxies)  # Shuffle to use random proxies
    
    for proxy in proxies:
        try:
            response = requests.get(url, proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"}, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            continue  # Try the next proxy if one fails
            
    return None  # If all proxies fail

@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

@app.route("/player_stats")
def get_nba_player_stats():
    player_id = 2544  # LeBron James (Example)
    url = f"https://stats.nba.com/stats/playergamelogs?Season=2023-24&PlayerID={player_id}"
    
    data = fetch_with_proxy(url)
    
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch player stats", "details": "All proxies failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)