import json
from io import BytesIO
from typing import Tuple

from environs import Env
from flask import Blueprint, Response, jsonify, render_template, request, redirect, url_for

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

@arb.route('/.env', methods=['GET'])
def hasker():
    from flask.json import jsonify
    return jsonify(**{'status': 'You are facking idiot', 'message': "stop hacking my site, i'm just a junior"})


@arb.route('/', methods=['GET', 'POST'])
def redirect_to_home():
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
    return redirect(f'/{LANG}')

@arb.route('/<lang>', methods=['GET'])
def form(lang: str = LANG):
    
    lang_map = {lang.value: lang for lang in Languages}
    lang = lang_map.get(lang, False)
    if not lang:
        return redirect(url_for('arb.form', lang=LANG))
    
    translations = Translation.query.filter_by(language_code=lang)
    
    context = {item.context_key: item.value for item in translations}
    context['LANG'] = lang._value_
    context['languages'] = lang_map.keys()
    
    return render_template('arb-main-form.html', **context)
