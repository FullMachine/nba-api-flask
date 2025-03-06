from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# Function to scrape fresh proxies from SSL Proxies website
def fetch_proxies():
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    proxies = []
    for row in soup.select("table tbody tr")[:10]:  # Get top 10 proxies
        tds = row.find_all("td")
        proxy = f"http://{tds[0].text}:{tds[1].text}"  # IP:PORT format
        proxies.append(proxy)

    return proxies if proxies else ["http://52.73.224.54:3128"]  # Fallback proxy

# Function to get a random proxy from the scraped list
def get_random_proxy():
    return random.choice(fetch_proxies())

# Default route to check if API is running
@app.route("/")
def home():
    return jsonify({"message": "NBA API is running with proxy rotation!"})

# NBA Player Stats Route
@app.route("/player_stats")
def get_nba_player_stats():
    url = "https://stats.nba.com/stats/playergamelogs"
    params = {
        "Season": "2023-24",
        "PlayerID": "2544",
    }

    for attempt in range(5):  # Try 5 different proxies
        proxy = get_random_proxy()
        proxies = {"http": proxy, "https": proxy}

        try:
            response = requests.get(url, params=params, proxies=proxies, timeout=15)
            response.raise_for_status()
            return jsonify(response.json())  # Success ✅

        except requests.RequestException as e:
            print(f"Proxy failed ({proxy}): {e}")  # Debugging info

    return jsonify({"error": "Failed to fetch player stats", "details": "All proxies failed"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure dynamic PORT for Render
    app.run(host="0.0.0.0", port=port)