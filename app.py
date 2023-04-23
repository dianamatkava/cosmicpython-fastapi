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
        # SERVER_NAME = env.str('SERVER_NAME', default='ef8b-2001-9e8-2866-a700-adf3-fe8d-9ec8-24c7.ngrok-free.app'),
        FLASK_APP = env.str('FLASK_APP', default='app.py'),
        FLASK_DEBUG = env.str('FLASK_DEBUG', default=True),
        SECRET_KEY = env.str(
            'SECRET_KEY', default='MY_SECRET_KEY'
        ),
        SQLALCHEMY_DATABASE_URI = env.str(
            'SQLALCHEMY_DATABASE_URI', default='sqlite:///arb.sqlite3'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS = True,
        FLASK_ADMIN_SWATCH = 'cerulean'
    )
        
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
    
        
    # class ProtectAdminMiddleware:
    #     def __init__(self, app):
    #         self.app = app
    #         self.prefix = '/admin'

    #     def __call__(self, environ, start_response):
    #         if environ['PATH_INFO'].startswith(self.prefix):
    #             if not current_user or not current_user.is_authenticated:
    #                 URL = environ['SERVER_NAME'] + '/auth/login'
    #                 start_response('301', [('Location', URL)])
    #                 return ["Redirecting to application...".encode()]
    #              
    #         return self.app(environ, start_response)
        
    # Register admin views
    admin.add_view(ModelView(CustomerData, db.session))
    admin.add_view(ModelView(Translation, db.session))
    
    # Register middleware
    # app.wsgi_app = ProtectAdminMiddleware(app.wsgi_app)
    
    # Register blueprints
    from auth.routes import auth as blueprint
    app.register_blueprint(blueprint)
    
    from arb.routes import arb
    app.register_blueprint(arb)

    return app

app = create_app()
