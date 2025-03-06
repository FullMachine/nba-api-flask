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
        headers = logs.get_dict()["resultSets"][0]["headers"]  # Get column names

        # Find the correct index for each stat dynamically
        stat_indices = {
            "PLAYER_NAME": headers.index("PLAYER_NAME"),
            "TEAM_NAME": headers.index("TEAM_NAME"),
            "GAME_DATE": headers.index("GAME_DATE"),
            "MATCHUP": headers.index("MATCHUP"),
            "MIN": headers.index("MIN"),
            "PTS": headers.index("PTS"),  # ✅ Ensure correct index for points
            "AST": headers.index("AST"),
            "REB": headers.index("REB"),
            "STL": headers.index("STL"),
            "BLK": headers.index("BLK"),
            "TOV": headers.index("TOV")
        }

        return {
            "player": latest_game[stat_indices["PLAYER_NAME"]],
            "team": latest_game[stat_indices["TEAM_NAME"]],
            "game_date": latest_game[stat_indices["GAME_DATE"]],
            "matchup": latest_game[stat_indices["MATCHUP"]],
            "minutes": latest_game[stat_indices["MIN"]],
            "points": latest_game[stat_indices["PTS"]],  # ✅ Now dynamically fetched
            "assists": latest_game[stat_indices["AST"]],
            "rebounds": latest_game[stat_indices["REB"]],
            "steals": latest_game[stat_indices["STL"]],
            "blocks": latest_game[stat_indices["BLK"]],
            "turnovers": latest_game[stat_indices["TOV"]]
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