#-*- coding=utf-8 -*-

from datetime import datetime
from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
import json
from datetime import datetime
import sys

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


URI = os.environ.get('MONGODB_URI')
client = MongoClient(URI)
db = client['heroku_95w86hmz']
collection = db['thairath']

@app.route('/api')
def disp_news():
    date = request.args.get('date', type=str)
    tag = request.args.get('tag', type=str)
    limit = request.args.get('limit', type=int, default=5)


    query = {}
    if tag is not None:
        query = {"tags": {"$elemMatch": {"$eq": tag} } }
    if date is not None:
        query = {"pub_date": date}
    if (date is not None) and (tag is not None):
        query = {"$and": [{"tags": {"$elemMatch": {"$eq": tag} } }, {"pub_date": date}] }

    cursor = collection.find(query, projection={"_id":0}, limit=limit)
    print(cursor.count())
    results = []
    for doc in cursor:
        results.append(doc)
    return jsonify(results)

if __name__ == "__main__":
    
    app.run()
