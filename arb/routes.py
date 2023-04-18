import json
from io import BytesIO
from typing import Tuple

from environs import Env
from flask import Blueprint, Response, jsonify, render_template, request, redirect

from arb.models import CustomerData, Languages, Translation
from extensions import db
from shared.validations import validate_email, validate_phone_number

env = Env()
env.read_env()

arb = Blueprint('arb', __name__, url_prefix='/')

LANG = env.str('DEFAULT_LANG', default='EN').lower()


def validate_user_input(data: dict) -> Tuple[bool, dict]:
        if not validate_email(data['email']):
            return False, {'message': 'Email not valid'}
        if not validate_phone_number(data['phone']):
            return False, {'message': 'Phone number not valid'}
        if CustomerData.query.filter_by(email=data['email']).count():
            return False, {'message': 'Email already exist'}
        return True, ''

@arb.route('/', methods=['GET'])
def redirect_to_home():
    return redirect(f'/{LANG}')

@arb.route('/<lang>', methods=['GET', 'POST'])
def form(lang: str = LANG):
    lang = Languages.__getattribute__(Languages, lang.upper())
    translations = Translation.query.filter_by(language_code=lang)
    context = {item.context_key: item.value for item in translations}
    context['LANG'] = lang._value_
    context['languages'] = [lang.lower() for lang in Languages._member_names_]
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