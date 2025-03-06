from flask import Flask, jsonify
import os
import logging
import time
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.library.http import NBAStatsHTTP

app = Flask(__name__)

# Enable Logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

# Function to fetch NBA player stats with error handling
@app.route("/player_stats")
def get_nba_player_stats():
    try:
        headers = {
            "Host": "stats.nba.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "x-nba-stats-origin": "stats",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.nba.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }

        # Use NBAStatsHTTP with headers to avoid being blocked
        logs = playergamelogs.PlayerGameLogs(
            season_nullable='2023-24',
            player_id_nullable=2544,
            timeout=10
        )

        latest_game = logs.get_dict()["resultSets"][0]["rowSet"][0]

        stats = {
            "player": latest_game[2],  # Player Name
            "team": latest_game[4],    # Team Abbreviation
            "game_date": latest_game[6],  # Game Date
            "points": latest_game[24],  # Points
            "assists": latest_game[19],  # Assists
            "rebounds": latest_game[18]  # Rebounds
        }
        return jsonify(stats)

    except Exception as e:
        app.logger.error(f"Error fetching player stats: {str(e)}")
        return jsonify({"error": "Failed to fetch player stats", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)