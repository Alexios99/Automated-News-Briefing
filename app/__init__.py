from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'devsecret')
    from .routes import main
    app.register_blueprint(main)
    return app 