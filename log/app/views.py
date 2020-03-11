from app import app
from flask import request, jsonify, make_response
import requests
import pandas as pd
import os
import json

@app.route('/')
def index():
    return "Hello from Log"


@app.route('/log', methods=['POST'])
def log():
    data = json.loads(request.data)
    req_time = data["req_time"]
    keyword = data["keyword"]
    if not os.path.isfile('req_time.csv'):
        df_req = pd.DataFrame(columns=["Req_Time", "Keyword"])
        df_req.to_csv(r'req_time.csv', index=False, header=True)

    df_req = pd.read_csv('req_time.csv')
    df_req = df_req.append(pd.Series({
        "Req_Time": req_time,
        "Keyword": keyword
    }),
                           ignore_index=True)
    df_req.to_csv(r'req_time.csv', index=False, header=True)

    if not os.path.isfile('count.csv'):
        df_count = pd.DataFrame(columns=["Keyword", "Count"])
        df_count.to_csv(r'count.csv', index=False, header=True)

    df_count = pd.read_csv('count.csv')
    row = df_count.loc[df_count["Keyword"] == keyword]
    if row.empty:
        df_count = df_count.append(pd.Series({
            "Keyword": keyword,
            "Count": 1
        }),
                                   ignore_index=True)
    else:
        df_count.at[row.index, "Count"] = row["Count"] + 1
    df_count.to_csv(r'count.csv', index=False, header=True)
    return make_response('OK', 200)

@app.route('/get_log', methods=['GET'])
def get_log():
    df_count = pd.read_csv('count.csv')
    return make_response(df_count.to_json(orient='index'), 200)
