from flask import Flask, jsonify, request
from nba_api.stats.endpoints import playergamelogs

app = Flask(__name__)

# Default home route
@app.route('/')
def home():
    return jsonify({"message": "NBA API is running!"})

# API route to get player stats
@app.route('/player_stats', methods=['GET'])
def get_nba_player_stats():
    player_name = request.args.get('player')

    if not player_name:
        return jsonify({"error": "Please provide a player name"}), 400

    try:
        logs = playergamelogs.PlayerGameLogs(season_nullable='2023-24')
        stats = logs.get_dict()

        return jsonify(stats)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)