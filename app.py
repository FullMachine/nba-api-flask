from flask import Flask, jsonify
import json
from nba_api.stats.endpoints import playergamelogs

app = Flask(__name__)

@app.route('/player_stats')
def player_stats():
    player_id = 2544  # LeBron James' ID
    season = '2024-25'

    # Fetch the latest game logs
    logs = playergamelogs.PlayerGameLogs(season_nullable=season, player_id_nullable=player_id)
    game_logs = logs.get_dict()["resultSets"][0]["rowSet"]

    if not game_logs:
        return jsonify({"error": "No game data found"}), 404

    # Extract the latest game
    latest_game = game_logs[0]

    # Correct indexes based on NBA API response
    game_data = {
        "season": latest_game[0],  
        "player_id": latest_game[1],  
        "player": latest_game[2],  
        "team_name": latest_game[6],  
        "game_id": latest_game[7],  
        "game_date": latest_game[8],  
        "matchup": latest_game[9],  
        "game_result": latest_game[10],  
        "minutes": round(float(latest_game[11]), 2),  
        "fgm": int(latest_game[12]),  
        "fga": int(latest_game[13]),  
        "fg_percentage": round(float(latest_game[14]), 3),  
        "3pm": int(latest_game[15]),  
        "3pa": int(latest_game[16]),  
        "3p_percentage": round(float(latest_game[17]), 3),  
        "ftm": int(latest_game[18]),  
        "fta": int(latest_game[19]),  
        "ft_percentage": round(float(latest_game[20]), 3),  
        "oreb": int(latest_game[21]),  
        "dreb": int(latest_game[22]),  
        "total_rebounds": int(latest_game[23]),  
        "assists": int(latest_game[24]),  
        "turnovers": int(latest_game[25]),  
        "steals": int(latest_game[26]),  
        "blocks": int(latest_game[27]),  
        "personal_fouls": int(latest_game[30]),  
        "points": int(latest_game[31]),  
        "plus_minus": int(latest_game[32]),  
    }

    return app.response_class(
        response=json.dumps(game_data, indent=4),  # Pretty-print JSON
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(debug=True)