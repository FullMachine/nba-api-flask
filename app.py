from flask import Flask, jsonify
import requests
import random
import os

app = Flask(__name__)

# ✅ List of free proxies (Update this frequently)
PROXIES = [
    "http://52.73.224.54:3128",
    "http://204.236.137.68:80",
    "http://160.20.55.235:8080",
    "http://3.90.100.12:80",
    "http://34.244.90.35:80",
]

def get_random_proxy():
    """Pick a random proxy from the list"""
    return random.choice(PROXIES)

def get_nba_player_stats():
    """Fetch NBA player stats with rotating proxies"""
    url = "https://stats.nba.com/stats/playergamelogs"
    params = {
        "Season": "2023-24",
        "PlayerID": "2544",  # Example: LeBron James' Player ID
    }

    for attempt in range(len(PROXIES)):  # Try different proxies
        proxy = get_random_proxy()
        proxies = {"http": proxy, "https": proxy}

        try:
            response = requests.get(url, params=params, proxies=proxies, timeout=10)
            response.raise_for_status()  # Raise error if request fails
            return response.json()  # Return data if successful

        except requests.RequestException as e:
            print(f"Proxy failed ({proxy}): {e}")

    return {"error": "Failed to fetch player stats", "details": "All proxies failed"}

@app.route("/")
def home():
    """Default route to check if API is running"""
    return jsonify({"message": "NBA API is running!"})

@app.route("/player_stats")
def player_stats():
    """Route to fetch NBA player stats"""
    data = get_nba_player_stats()
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure PORT is dynamic for Render
    app.run(host="0.0.0.0", port=port)