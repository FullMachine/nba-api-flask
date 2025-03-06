from flask import Flask, jsonify
import os

app = Flask(__name__)

# Default route to check if API is running
@app.route("/")
def home():
    return jsonify({"message": "NBA API is running!"})

# Example NBA player stats route (replace with actual API logic)
@app.route("/player_stats")
def get_player_stats():
    return jsonify({
        "player": "LeBron James",
        "points": 30,
        "assists": 8,
        "rebounds": 10
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure PORT is dynamic for Render
    app.run(host="0.0.0.0", port=port)