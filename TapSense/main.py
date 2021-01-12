from flask import Flask, render_template, request, jsonify, make_response, redirect
from models.database import init_db, db_session, clear_db
from models.models import TapRecord
import json
import random
app = Flask(__name__)

sent_map = {
    0: "Once when I was a teenager, my father and I were standing in line to buy tickets for the circus. Finally, there was only one family between us and the ticket counter.",
    1: "One night a group of nomads were preparing to retire for the evening when suddenly they were surrounded by a great light. They knew they were in the presence of a celestial being.",
    2: "On my first day of teaching, all my classes were going well. Being a teacher was going to be a cinch, I decided. Then came period seven, the last class of the day.",
    3: "The store owner smiled and whistled and out of the kennel came Lady, who ran down the aisle of his store followed by five teeny, tiny balls of fur. One puppy was lagging considerably behind.",
    4: "I have a friend named Monty Roberts who owns a horse ranch in San Ysidro. He has let me use his house to put on fund-raising events to raise money for youth at risk programs."
}

@app.route('/', methods=['GET'])
def root():
    sentence = sent_map[random.randrange(len(sent_map))]
    return render_template('index.html', sentence=sentence)

@app.route('/success', methods=['POST'])
def success():
    print(request.method)
    print(request.json)
    print(request.json["timestamps"])
    print(request.json["error_count"])
    return_json = {
        "timestamps": request.json["timestamps"],
        "error_count": request.json["error_count"]
    }
    return jsonify(ResultSet=json.dumps(return_json))

@app.route('/add_data', methods=['POST'])
def add_data():
    s = " ".join(map(str, request.json['timestamps']))
    c = TapRecord(request.json["error_count"], s, request.json["name"])
    db_session.add(c)
    db_session.commit()
    print(request.json)
    return "success"

@app.route('/init', methods=['GET'])
def init():
    init_db()
    return "Initialize database"

@app.route('/clear', methods=['GET'])
def clear():
    clear_db()
    return redirect('/init')

@app.route('/check_data', methods=['GET'])
def check_data():
    all_data = TapRecord.query.all()
    return render_template('data.html', all_data=all_data)