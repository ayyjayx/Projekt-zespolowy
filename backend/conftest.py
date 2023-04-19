from app import create_app
from config import TestingConfig
from models import db as _db
import pytest

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        _db.init_app(app)
        _db.create_all()

    yield app

    with app.app_context():
        _db.drop_all()