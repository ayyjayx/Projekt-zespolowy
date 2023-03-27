from flask import Flask
from routes import init_routes


def create_app(test_config=None):

    # creates an application that is named after the name of the file
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "some_dev_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:projekt1234@database:5432/postgres"

    # initializing routes
    init_routes(app)

    return app
