from flask import Flask, jsonify
from nba_api.stats.endpoints import playergamelogs

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "NBA API is running!"})

@app.route('/player_stats', methods=['GET'])
def get_nba_player_stats():
    try:
        # Fetching LeBron James' game logs for the current season
        logs = playergamelogs.PlayerGameLogs(season_nullable='2023-24', player_id_nullable=2544)
        data = logs.get_dict()

        # Extract the latest game
        latest_game = data['resultSets'][0]['rowSet'][0]

        response = {
            "player": "LeBron James",
            "points": latest_game[24],
            "assists": latest_game[19],
            "rebounds": latest_game[20]
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": "Failed to fetch player stats", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)