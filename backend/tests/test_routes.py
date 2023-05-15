import json
from app import app, db
from models import Account
from flask_jwt_extended import create_access_token
from pytest_mock import mocker
from datetime import datetime, timezone, timedelta
from freezegun import freeze_time

def test_registration_success(client):
    response = client.post(
        "/registration",
        json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "testpassword",
            "passwordRepeat": "testpassword",
        },
    )

    assert response.status_code == 201
    assert b"Successfully registered." in response.data


def test_registration_existing_account(app, client, new_account):
    with app.app_context():
        db.session.add(new_account)
        db.session.commit()

        response = client.post(
            "/registration",
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "testpassword",
                "passwordRepeat": "testpassword",
            },
        )

        assert response.status_code == 202
        assert b"Account already exists." in response.data

        db.session.delete(new_account)
        db.session.commit()


def test_registration_different_passwords(client):
    response = client.post(
        "/registration",
        json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "testpassword",
            "passwordRepeat": "differentpassword",
        },
    )

    assert response.status_code == 202
    assert b"Passwords do not match" in response.data


def test_registration_data_lenght(client):
    response = client.post(
        "/registration",
        json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "tes",
            "passwordRepeat": "tes",
        },
    )

    assert response.status_code == 202
    assert b"Password must be >=4 characters long" in response.data


def test_registration_missing_data(client):
    response = client.post(
        "/registration",
        json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 202
    assert b"Missing data" in response.data


def test_registration_use_POST(client):
    response = client.get(
        "/registration",
        json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200
    assert b"Use POST" in response.data


def test_login_success(app, client):
    with app.app_context():
        account = Account(username="testuser", email="testuser@test.com")
        account.set_password("testpassword")
        db.session.add(account)
        db.session.commit()

        response = client.post(
            "/login",
            json={
                "username": "testuser",
                "password": "testpassword",
            },
        )

        assert b"access_token" in response.data
        assert b"refresh_token" in response.data


def test_login_incorrect_password(app, client, new_account):
    with app.app_context():
        db.session.add(new_account)
        db.session.commit()

        response = client.post(
            "/login",
            json={
                "username": "testuser",
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 200
        assert b"Incorrect Password." in response.data


def test_login_missing_data(app, client, new_account):
    with app.app_context():
        db.session.add(new_account)
        db.session.commit()

        response = client.post(
            "/login",
            json={
                "username": "testuser",
            },
        )

        assert response.status_code == 201
        assert b"Missing data." in response.data


def test_login_no_account(client):
    response = client.post(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == 200
    assert b"Account does not exist." in response.data


def test_login_use_POST(client):
    response = client.get(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == 201
    assert b"Use POST" in response.data

def test_show_account_no_account(app, client, new_account):
    with app.app_context():
        token = create_access_token(identity=new_account.id)
        client.set_cookie('localhost', 'access_token_cookie', token)
        response = client.get(
            "/profile"
        )
        assert b'Account does not exist.' in response.data

def test_show_account_token_expired(app, client, new_account):
    with app.app_context():
        expires_delta = timedelta(seconds=1)
        token = create_access_token(identity=new_account.id, expires_delta=expires_delta)
        expired_timestamp = datetime.fromtimestamp(datetime.timestamp(datetime.now(timezone.utc)) + 2, timezone.utc)

        with freeze_time(expired_timestamp):
            client.set_cookie('localhost', 'access_token_cookie', token)

            response = client.get('/profile')

            assert response.status_code == 401
            assert b'Token has expired' in response.data

def test_show_account(app, client, new_account):
    with app.app_context():
        expires_delta = timedelta(seconds=1)
        token = create_access_token(identity=new_account.id, expires_delta=expires_delta)
        expired_timestamp = datetime.fromtimestamp(datetime.timestamp(datetime.now(timezone.utc)) + 2, timezone.utc)

        with freeze_time(expired_timestamp):
            client.set_cookie('localhost', 'access_token_cookie', token)

            response = client.get('/profile')
