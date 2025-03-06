from flask import Flask, jsonify

app = Flask(__name__)

# Home route (working)
@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

# Player stats route (not working, so we fix it)
@app.route("/player_stats")
def get_player_stats():
    return jsonify({
        "player": "LeBron James",
        "points": 30,
        "assists": 8,
        "rebounds": 10
    })

if __name__ == "__main__":
    app.run(debug=True)