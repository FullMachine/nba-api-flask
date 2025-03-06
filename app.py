from flask import Flask, jsonify
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Step 1: Function to Scrape Fresh Proxy List
def get_fresh_proxies():
    url = "https://sslproxies.org/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table containing proxies
        table = soup.find("table", {"class": "table-striped"})

        if not table:
            return None  # No table found

        proxies = []
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue  # Skip invalid rows
            
            ip = cols[0].text.strip()
            port = cols[1].text.strip()
            proxy = f"{ip}:{port}"
            proxies.append(proxy)

        if not proxies:
            return None  # No proxies found

        return proxies
    except Exception as e:
        return None  # Return None if scraping fails

# ✅ Step 2: Function to Fetch NBA Stats with Proxy Rotation
def fetch_with_proxy(url):
    proxies = get_fresh_proxies()

    if not proxies:
        return {"error": "Failed to fetch player stats", "details": "No working proxies available"}

    for proxy in proxies:
        try:
            proxy_dict = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
            response = requests.get(url, proxies=proxy_dict, timeout=10)
            
            if response.status_code == 200:
                return response.json()  # Successful request
        except requests.RequestException:
            continue  # Try the next proxy

    return {"error": "Failed to fetch player stats", "details": "All proxies failed"}

# ✅ Step 3: Default Route
@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

# ✅ Step 4: NBA Player Stats Route
@app.route("/player_stats")
def get_nba_player_stats():
    nba_api_url = "https://stats.nba.com/stats/playergamelogs?Season=2023-24&SeasonType=Regular+Season"
    data = fetch_with_proxy(nba_api_url)
    return jsonify(data)

# ✅ Step 5: Run Flask App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure PORT is dynamic for Render
    app.run(host="0.0.0.0", port=port)