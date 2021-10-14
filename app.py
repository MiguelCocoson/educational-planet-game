from flask import Flask, render_template

app = Flask(__name__)

@app.route("/planets-game")
def planets_game():
    return render_template("planets-game.html")