import json
from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    return json.dumps({'status': 'OK'})