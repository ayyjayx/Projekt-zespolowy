from app import create_app
from config import TestingConfig
from models import Account, ResetToken, Game, db as _db
import pytest
from flask_jwt_extended import JWTManager
import uuid


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


@pytest.fixture
def new_token():
    token = ResetToken(username="testuser", token="testtoken")
    return token


@pytest.fixture
def new_game():
    game = Game(id=1, fen="new_fen", player_one_id=1)
    return game
