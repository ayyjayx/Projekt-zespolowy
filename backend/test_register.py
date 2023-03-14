from app import app
from models import db, Account

def test_register():
    with app.test_client() as client:
        response = client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'testuser@test.com'
        })
        assert b'Udana rejestracja' in response.data
