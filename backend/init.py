from flask import Flask
from routes import init_auth_routes, init_profile_routes
from config import DevelopmentConfig


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_profile_routes(app)
    init_auth_routes(app)

    return app
