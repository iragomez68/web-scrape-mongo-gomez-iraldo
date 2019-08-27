from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import databaseconfig as cfg

# Setup the databaseconfig.py with the required information depending on 
# whether you are using local or Atlas (cloud) MongoDb
# The databaseconfig.py file contains a datadict with the following structure:
# msql = { 'server' : '<server_name>',      #Atlas -> 'mongodb+srv'
                                            #local -> 'mongodb'
#          'username': '<username>',        #Atlas -> username 
                                            #local -> 'localhost'
#          'passwd': '<password>',          #Atlas -> passwd for user name
                                            #local -> port number 27017 (default)
#          'cluster': '<mongodb_cluster>',  #Atlas -> cluster name including @
                                            #local -> ''
#          'database': '<database>'}        #Atlas -> databasename?retryWrites=true&w=majority  
                                            #      -> databasename

# For local MongoDB the use definition below for the databasecofig.py
# Local MongoDB connection information
# msql = { 'server' : 'mongodb',                        #default: mongodb,
#          'username': 'localhost',                     #localhost
#          'passwd': '27017',                           #portnumber
#          'cluster': '',                               #leave empty
#          'database': 'mars_app'}                      #databasename

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
connection_string = (f"{cfg.msql['server']}://{cfg.msql['username']}:{cfg.msql['passwd']}{cfg.msql['cluster']}/{cfg.msql['database']}")
# print(connection_string)

mongo = PyMongo(app, uri=connection_string)
mongo.db.mars.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    print(mars_data)

    # Return template and data
    if mars_data != None:
        return render_template("index.html", mars=mars_data)
    else:
        return render_template("index.html", mars={"mars_facts": {"value": {"no_content":"Press the Button"}}})

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    marsdata = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, marsdata, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
