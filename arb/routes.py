import json
from io import BytesIO
from typing import Tuple

from flask import Blueprint, Response, jsonify, render_template, request

from arb.models import CustomerData
from extensions import db
from shared.validations import validate_email, validate_phone_number

arb = Blueprint('arb', __name__, url_prefix='/')

def validate_user_input(data: dict) -> Tuple[bool, dict]:
        if not validate_email(data['email']):
            return False, {'message': 'Email not valid'}
        if not validate_phone_number(data['phone']):
            return False, {'message': 'Phone number not valid'}
        if CustomerData.query.filter_by(email=data['email']).count():
            return False, {'message': 'Email already exist'}
        return True, ''

@arb.route('/', methods=['GET', 'POST'])
def form():
    context = {}
    if request.method == "POST":
        
        data = json.load(BytesIO(request.data))
        status, res = validate_user_input(data)
        if not status:
            return jsonify(res)
        try:
            customer = CustomerData(**data)
            db.session.add(customer)
            db.session.commit()
        except Exception as _ex:
            return Response(status=400, response=_ex)
        return Response(status=200)
    return render_template('arb-form.html', context=context)