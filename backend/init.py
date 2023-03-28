from flask import Flask
from routes import init_routes

from config import DevelopmentConfig


def create_app(test_config=None):

    # creates an application that is named after the name of the file
    app = Flask(__name__)

    app.config(DevelopmentConfig)

    # initializing routes
    init_routes(app)

    return app
