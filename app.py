from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


if __name__ == '__main__':
    app.run()

@app.route("/planets-game")
def planets_game():
    return render_template("planets.html")

@app.route("/results", methods=["POST"])
def results():
    req = request.form
    planet1 = req["planet1"]
    planet2 = req["planet2"]
    planet3 = req["planet3"]
    planet4 = req["planet4"]
    planet5 = req["planet5"]
    planet6 = req["planet6"]
    planet7 = req["planet7"]
    planet8 = req["planet8"]

    all_planets = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8]
    planets_list = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]

    return render_template("results.html", all_planets=all_planets, planets_list=planets_list)

