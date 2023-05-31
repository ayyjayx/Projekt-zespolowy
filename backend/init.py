from config import DevelopmentConfig
from flask import Flask
from routes import init_routes


def create_app(test_config=None):
    app = Flask(__name__, static_folder="frontend/build", static_url_path="")
    app.config.from_object(DevelopmentConfig)

    init_routes(app)
    return app
