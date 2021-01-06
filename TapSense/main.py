from flask import Flask, render_template, request, jsonify, make_response
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
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

@app.route('/data', methods=['POST'])
def data():
    print(request.json)
    return make_response(request.json)