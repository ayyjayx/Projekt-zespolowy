import json
from app import app, db
from models import Account, JWTTokenBlocklist
import pytest


def test_registration_success(app, client):
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


def test_registration_existing_account(app, client):
    with app.app_context():
        account = Account(username="testuser", email="testuser@test.com")
        account.set_password("testpassword")
        db.session.add(account)
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

        db.session.delete(account)
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


def test_login_incorrect_password(app, client):
    with app.app_context():
        account = Account(username="testuser", email="testuser@test.com")
        account.set_password("testpassword")
        db.session.add(account)
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


def test_login_missing_data(app, client):
    with app.app_context():
        account = Account(username="testuser", email="testuser@test.com")
        account.set_password("testpassword")
        db.session.add(account)
        db.session.commit()

        response = client.post(
            "/login",
            json={
                "username": "testuser",
            },
        )

        assert response.status_code == 201
        assert b"Missing data." in response.data


def test_login_no_account(app, client):
    response = client.post(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == 200
    assert b"Account does not exist." in response.data


def test_login_no_account(app, client):
    response = client.post(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == 200
    assert b"Account does not exist." in response.data


def test_login_use_POST(app, client):
    response = client.get(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == 201
    assert b"Use POST" in response.data
