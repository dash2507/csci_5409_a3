from app import app
from flask import request, jsonify, make_response
import os
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import json


@app.route('/')
def index():
    return "Hello From Catalogue"


def fetch_data(keyword):
    client = MongoClient('mongodb://mongodb:27017/')
    db = client.gu_books
    doc = db.books.find_one({'title': keyword})
    if doc != None:
        print(doc)
    return doc


@app.route('/catalogue')
def notes():
    keyword = request.args.get('keyword')
    if not os.path.isfile("catalogue.csv"):
        df = pd.DataFrame(columns=["Keyword", "Author"])
        df.to_csv("catalogue.csv", index=False, header=True)
    df = pd.read_csv('catalogue.csv')
    df["Author"] = df.Author.astype(str)
    row = df[df["Keyword"] == keyword]
    if row.empty:
        doc = fetch_data(keyword)
        if doc == None:
            return jsonify(code=0, text='No Recored Found')
        df = df.append({
            'Keyword': keyword,
            'Author': doc['author']
        },
                       ignore_index=True)
        df.to_csv("catalogue.csv", index=False, header=True)
        return make_response(
            jsonify(keyword=doc["title"], author=doc["author"], code=1), 200)
    else:
        res = json.loads(row.to_json(orient='records')[1:-1])
        res["code"] = 1
        return make_response(jsonify(res), 200)
