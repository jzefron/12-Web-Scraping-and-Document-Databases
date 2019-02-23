from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)
#db = mongo['mars_db']


@app.route("/scrape")
def scrape():
    scrape_data = scrape_mars.scrape()
    mongo.db.mars.drop()
    print(scrape_data)
    mongo.db.mars.insert_one( scrape_data)
   
    return redirect("/")

@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()
    return render_template('index.html',data = mars_data)
    


if __name__ == '__main__':
    app.run(debug=True)
