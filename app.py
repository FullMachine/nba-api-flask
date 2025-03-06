from flask import Flask, jsonify
from nba_api.stats.endpoints import playergamelogs

app = Flask(__name__)

# Function to fetch the latest game stats for LeBron James
def get_latest_game_stats():
    try:
        logs = playergamelogs.PlayerGameLogs(season_nullable='2024-25', player_id_nullable=2544)
        game_logs = logs.get_dict()["resultSets"][0]["rowSet"]

        if not game_logs:
            return None

        latest_game = game_logs[0]  # Get most recent game

        # Verify correct indices for each stat
        return {
            "player": latest_game[2],      # Player Name
            "team": latest_game[6],        # Team Name
            "game_date": latest_game[8],   # Game Date
            "matchup": latest_game[9],     # Matchup
            "minutes": latest_game[11],    # Minutes Played
            "points": latest_game[30],     # ✅ Corrected Points Index
            "assists": latest_game[25],    # Assists
            "rebounds": latest_game[23],   # ✅ Corrected Rebounds Index
            "steals": latest_game[26],     # Steals
            "blocks": latest_game[27],     # Blocks
            "turnovers": latest_game[28]   # Turnovers
        }
    
    except Exception as e:
        return {"error": f"Failed to fetch stats: {str(e)}"}

@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

@app.route("/player_stats")
def player_stats():
    stats = get_latest_game_stats()
    if stats:
        return jsonify(stats)
    else:
        return jsonify({"error": "No data available"}), 500

if __name__ == "__main__":
    app.run(debug=True)