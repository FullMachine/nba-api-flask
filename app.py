from flask import Flask, jsonify, request
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.static import players

app = Flask(__name__)

def get_player_id(player_name):
    """Find player ID based on player name."""
    nba_players = players.get_players()
    for player in nba_players:
        if player['full_name'].lower() == player_name.lower():
            return player['id']
    return None

def get_nba_player_stats(player_name):
    """Fetch recent game logs for a player using their Player ID."""
    player_id = get_player_id(player_name)
    if not player_id:
        return {"error": "Player not found"}

    logs = playergamelogs.PlayerGameLogs(player_id_nullable=player_id, season_nullable='2023-24')
    return logs.get_dict()

@app.route('/player_stats', methods=['GET'])
def player_stats():
    """API endpoint to fetch player stats."""
    player_name = request.args.get('player', 'LeBron James')  # Default: LeBron James
    data = get_nba_player_stats(player_name)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)