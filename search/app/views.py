from app import app
import requests
from flask import request, jsonify, make_response
import datetime
import json


@app.route('/')
def index():
    return "Hello from Search"


@app.route('/search')
def search():
    query = request.args.get('query')
    log = {'req_time': datetime.datetime.now().strftime("%c"), \
            'keyword' : query
        }
    res_log = requests.post("http://log:5000/log", json=log)
    res_cat = requests.get("http://catalogue:5000/catalogue?keyword=" + query)
    r = make_response(res_cat.text, 200)
    r.mimetype = 'application/json'
    r.headers['Content-Type'] = 'application/json'
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r


@app.route('/notes')
def notes():
    keyword = request.args.get('keyword')
    res_notes = requests.get("http://notes:5000/notes?keyword=" + keyword)
    r = make_response(res_notes.text, 200)
    r.mimetype = 'application/json'
    r.headers['Content-Type'] = 'application/json'
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r


@app.route('/add_note')
def add_notes():
    keyword = request.args.get('keyword')
    note = request.args.get('note')
    req = {'keyword': keyword, 'note': note}
    res_notes = requests.post("http://notes:5000/add_note", json=req)
    r = make_response(res_notes.text, 200)
    r.mimetype = 'application/json'
    r.headers['Content-Type'] = 'application/json'
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r
