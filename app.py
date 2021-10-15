from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/planets-game", methods=["GET","POST"])
def planets_game():
    return render_template("planets.html")
