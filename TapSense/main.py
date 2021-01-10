from flask import Flask, render_template, request, jsonify, make_response
from models.database import init_db, db_session, clear_db
from models.models import TapRecord
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

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
    c = TapRecord(request.json["error_count"], s)
    db_session.add(c)
    db_session.commit()
    print(request.json)
    return

@app.route('/init', methods=['GET'])
def init():
    init_db()
    return "success"

@app.route('/clear', methods=['GET'])
def clear():
    clear_db()
    return "Delete data"

@app.route('/check_data', methods=['GET'])
def check_data():
    all_data = TapRecord.query.all()
    return render_template('data.html', all_data=all_data)