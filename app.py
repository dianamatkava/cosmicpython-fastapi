import os

from environs import Env
from flask import Flask, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from werkzeug.wrappers import Request

from arb.models import *
from auth.models import *
from extensions import admin, db, migrate

env = Env()
env.read_env()


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configs
    app.config.from_mapping(
        SERVER_NAME = env.str('SERVER_NAME', default='127.0.0.1:5000'),
        FLASK_APP = env.str('FLASK_APP', default='app.py'),
        FLASK_DEBUG = env.bool('FLASK_DEBUG', default=True),
        SECRET_KEY = env.str(
            'SECRET_KEY', default='MY_SECRET_KEY'
        ),
        SQLALCHEMY_DATABASE_URI = env.str(
            'SQLALCHEMY_DATABASE_URI', default='sqlite:///arb.sqlite3'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS = True,
        FLASK_ADMIN_SWATCH = 'cerulean'
    )
    # print(f"DEBAG {app.config.FLASK_DEBUG}")
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Registered extensions
    with app.app_context():
        db.init_app(app)
        db.create_all()
        
    
    # Apps
    migrate.init_app(app, db, render_as_batch=True)
    admin.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.before_request
    def protect_admin():
        if request.path.startswith('/admin'):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
    admin.add_view(ModelView(CustomerData, db.session))
    admin.add_view(ModelView(Translation, db.session))
    
    # Register blueprints
    from auth.routes import auth as blueprint
    app.register_blueprint(blueprint)
    
    from arb.routes import arb
    app.register_blueprint(arb)

    return app

app = create_app()
