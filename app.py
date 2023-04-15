import json
from flask import Flask, render_template


app = Flask(__name__)

# from posthog import Posthog

# posthog = Posthog(project_api_key='phc_itIdr55hO2OcvABciUtxLzXN8ppBBY0ewRCpN7gvwPQ', host='https://eu.posthog.com')

            
            
@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('arb-form.html')