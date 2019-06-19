from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("Stuff/index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_scrape = scrape_mars.scrape()
    mars.update(
        {},
        mars_scrape,
        upsert=True
    )
    return "Scraped is complete"


if __name__ == "__main__":
    app.run(debug=True)