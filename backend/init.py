from flask import Flask
from flask_cors import CORS
from routes import init_routes
from config import DevelopmentConfig


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_routes(app)

    return app
