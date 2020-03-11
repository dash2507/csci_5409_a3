from app import app
from flask import request, jsonify, make_response
import os
import json


@app.route('/')
def index():
    return "Hello From Note"


@app.route('/notes')
def notes():
    keyword = request.args.get('keyword')
    if not os.path.isfile('notes_stored/' + keyword):
        return make_response(jsonify(code=0, text="No Notes"), 200)

    with open("notes_stored/" + keyword, "r+") as file:
        notes = file.read()
        notes = notes.split("\n,=>\n")[:-1]
    return make_response(jsonify(code=1, notes=notes), 200)


@app.route('/add_note', methods=["POST"])
def add_notes():
    data = json.loads(request.data)
    keyword = data["keyword"]
    note = data["note"]
    if not os.path.isdir('notes_stored'):
        os.makedirs('notes_stored')
    with open("notes_stored/" + keyword, "a+") as file:
        file.write(note)
        file.write("\n,=>\n")
    return make_response(jsonify(code=1,text="OK"), 200)