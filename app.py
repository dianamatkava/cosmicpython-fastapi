import os
import json
from io import BytesIO
from environs import Env
from flask import Flask, render_template, request, Response
from flask import jsonify
from extensions import db, migrate
from arb.models import *
from shared.validations import validate_email, validate_phone_number


env = Env()
env.read_env()


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configs
    app.config.from_mapping(
        FLASK_APP = env.str('FLASK_APP', default='app.py'),
        FLASK_DEBUG = env.str('FLASK_DEBUG', default=True),
        SECRET_KEY = env.str(
            'SECRET_KEY', default='MY_SECRET_KEY'
        ),
        SQLALCHEMY_DATABASE_URI = env.str(
            'SQLALCHEMY_DATABASE_URI', default='sqlite:///arb.sqlite3'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS = True,
    )
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Registered extensions
    with app.app_context():
        db.init_app(app)
        db.create_all()
        
        
    migrate.init_app(app, db)

    def validate_user_input(data: dict) -> tuple[bool, dict]:
        if not validate_email(data['email']):
            return False, {'message': 'Email not valid'}
        if not validate_phone_number(data['phone']):
            return False, {'message': 'Phone number not valid'}
        if CustomerData.query.filter_by(email=data['email']).count():
            return False, {'message': 'Email already exist'}
        if CustomerData.query.filter_by(phone=data['phone']).count():
            return False, {'message': 'Phone number already exist'}
        return True, ''

    @app.route('/', methods=['GET', 'POST'])
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

    return app

app = create_app()

# from posthog import Posthog

# posthog = Posthog(project_api_key='phc_itIdr55hO2OcvABciUtxLzXN8ppBBY0ewRCpN7gvwPQ', host='https://eu.posthog.com')
