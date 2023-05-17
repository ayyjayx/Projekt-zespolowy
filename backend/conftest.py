from app import create_app
from config import TestingConfig
from models import Account, db as _db
import pytest
from flask_jwt_extended import JWTManager


@pytest.fixture
def app():
    app = create_app()
    jwt = JWTManager(app)
    app.config.from_object(TestingConfig)

    with app.app_context():
        _db.init_app(app)
        _db.create_all()

    yield app

    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def new_account():
    account = Account(email="pytest@test.com", username="testuser", admin=False)
    account.set_password("password")
    return account
