from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Use PyMongo to establish Mongo connection
# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client.mars_db
# collection = db.mars

# Create an instance of Flask
# app = Flask(__name__)

# Use PyMongo to establish Mongo Connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mongo_app")

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route('/')
def home():
	mars = mongo.db.mars.find_one()
	return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update({},data, upsert=True)
    return redirect('/', code = 302)

if __name__ == "__main__":
    app.run(debug=True)