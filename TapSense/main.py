from flask import Flask, render_template, request, jsonify, make_response, redirect, send_file
from models.database import init_db, db_session, clear_db
from models.models import TapRecord
import json, io
import random
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

sent_map = {
    0: "Once when I was a teenager, my father and I were standing in line to buy tickets for the circus. Finally, there was only one family between us and the ticket counter.",
    1: "One night a group of nomads were preparing to retire for the evening when suddenly they were surrounded by a great light. They knew they were in the presence of a celestial being.",
    2: "On my first day of teaching, all my classes were going well. Being a teacher was going to be a cinch, I decided. Then came period seven, the last class of the day.",
    3: "The store owner smiled and whistled and out of the kennel came Lady, who ran down the aisle of his store followed by five teeny, tiny balls of fur. One puppy was lagging considerably behind.",
    4: "I have a friend named Monty Roberts who owns a horse ranch in San Ysidro. He has let me use his house to put on fund-raising events to raise money for youth at risk programs.",
    5: "My wife, Tere, and I purchased a new car in December. Even though we had tickets to fly from California to Houston to visit her family for Christmas, we decided to drive to Texas to break in the new car.",
    6: "Les Brown and his twin brother were adopted by Mamie Brown, a kitchen worker and maid, shortly after their birth in a poverty-stricken Miami neighborhood."
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
    t = " ".join(map(str, request.json['timestamps']))
    k = " ".join(request.json['keys'])
    print(type(request.json["joy_sadness"]))
    print(request.json["keys"])
    c = TapRecord(request.json["error_count"], t, k, request.json["name"], \
        request.json["sentence_length"], request.json["joy_sadness"], \
        request.json["anger_fear"], request.json["trust_disgust"], \
        request.json["interest_distraction"], request.json["impression_pessimism"])
    db_session.add(c)
    db_session.commit()
    print(request.json)
    return "success"

@app.route('/init', methods=['GET'])
def init():
    init_db()
    return "Initialize database"

# @app.route('/clear', methods=['GET'])
# def clear():
#     clear_db()
#     return redirect('/init')

@app.route('/data', methods=['GET'])
def data():
    all_data = TapRecord.query.all()
    # print(all_data[0].joy_sadness)
    i = 0
    d = {}
    for data in all_data:
        d[i] = {
            "name": data.name,
            "error_count": data.error_count,
            "timestamps": data.timestamps,
            "keys": data.keys,
            "sentence_length": data.sentence_length,
            "joy_sadness": data.joy_sadness,
            "anger_fear": data.anger_fear,
            "trust_disgust": data.trust_disgust,
            "interest_distraction": data.interest_distraction,
            "impression_pessimism": data.impression_pessimism
        }
        i += 1
    return jsonify(d)

@app.route('/check_data', methods=['GET'])
def check_data():
    all_data = TapRecord.query.all()
    return render_template('data.html', all_data=all_data)

@app.route('/download', methods=['GET'])
def download():
    all_data = TapRecord.query.all()
    print("all_data: ", all_data)
    i = 0
    d = {}
    for data in all_data:
        d[i] = {
            "name": data.name,
            "error_count": data.error_count,
            "timestamps": data.timestamps,
            "keys": data.keys,
            "sentence_length": data.sentence_length,
            "joy_sadness": data.joy_sadness,
            "anger_fear": data.anger_fear,
            "trust_disgust": data.trust_disgust,
            "interest_distraction": data.interest_distraction,
            "impression_pessimism": data.impression_pessimism
        }
        i += 1
    
    s = json.dumps(d, indent=4, ensure_ascii=False)
    mem = io.BytesIO()
    mem.write(s.encode('utf-8'))
    mem.seek(0)

    ret = send_file(mem, mimetype='application/json', as_attachment=True, attachment_filename='data.json')
    return ret