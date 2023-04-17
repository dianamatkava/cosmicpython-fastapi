import json
from io import BytesIO
from typing import Tuple

from environs import Env
from flask import Blueprint, Response, jsonify, render_template, request

from arb.models import CustomerData, Translation, Languages
from extensions import db
from shared.validations import validate_email, validate_phone_number

env = Env()
env.read_env()

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
    lang_code = env.str('DEFAULT_LANG', default='EN')
    lang = Languages.__getattribute__(Languages, lang_code)
    translations = Translation.query.all()
    
    context = {item.context_key: item.value for item in translations}
    context['LANG'] = lang_code.lower()
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
    return render_template('arb-form.html', **context)