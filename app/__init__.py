from flask import Flask
from flask_session import Session
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'devsecret')
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    from .routes import main
    app.register_blueprint(main)
    return app 