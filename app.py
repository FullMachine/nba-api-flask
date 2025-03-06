from flask import Flask, jsonify
import os
from nba_api.stats.endpoints import playergamelogs

app = Flask(__name__)

# Default route to check if API is running
@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

# Fetch Live NBA Player Stats
@app.route("/player_stats")
def get_nba_player_stats():
    # Fetch LeBron James' latest game stats (replace with any player's ID)
    logs = playergamelogs.PlayerGameLogs(season_nullable='2023-24', player_id_nullable=2544)

    # Extract the latest game data
    if logs.get_dict()["resultSets"][0]["rowSet"]:
        latest_game = logs.get_dict()["resultSets"][0]["rowSet"][0]
        stats = {
            "player": latest_game[2],  # Player Name
            "team": latest_game[4],    # Team Abbreviation
            "game_date": latest_game[6],  # Game Date
            "points": latest_game[24],  # Points
            "assists": latest_game[19],  # Assists
            "rebounds": latest_game[18]  # Rebounds
        }
    else:
        stats = {"error": "No game data available"}

    return jsonify(stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure PORT is dynamic for Render
    app.run(host="0.0.0.0", port=port)