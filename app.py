from flask import Flask, jsonify, request
from nba_api.stats.endpoints import playergamelogs

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "NBA API is running!"})

# Player Stats Route
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
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)