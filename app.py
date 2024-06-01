from flask import Flask, jsonify
import subprocess
import pymongo
import os

app = Flask(__name__)

# Initialize MongoDB client using environment variable
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = pymongo.MongoClient(mongo_uri)
db = client["twitter_trending"]
collection = db["trends"]

@app.route('/run_script')
def run_script():
    # Run the Selenium script
    subprocess.run(["python", "selenium_script.py"])
    
    # Fetch the latest record from MongoDB
    latest_record = collection.find().sort([('_id', -1)]).limit(1)
    for record in latest_record:
        return jsonify(record)

if __name__ == '__main__':
    app.run(debug=True)
