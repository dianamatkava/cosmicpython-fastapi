import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('arb-form.html')