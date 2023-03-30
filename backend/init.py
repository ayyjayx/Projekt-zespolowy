from flask import Flask
from routes import init_routes
# import os

# folder templates jest w folderze frontend:
# template_dir = os.path.abspath('../../frontend/src')


def create_app(test_config=None):
    app = Flask(__name__)
    # po dodaniu templates do frontend:
    # app = Flask(__name__, template_folder=template_dir)

    app.config["SECRET_KEY"] = "some_dev_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "\
        postgresql://postgres:projekt1234@database:5432/postgres"

    init_routes(app)

    return app
