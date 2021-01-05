from flask import Flask, render_template, request
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/success', methods=['POST'])
def success():
    print(request.method)
    print(request.json)
    print(request.json["timespamps"])
    print(request.json["error_count"])
    return 'Success'