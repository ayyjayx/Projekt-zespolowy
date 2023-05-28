import json
from app import app, db
from models import Account
from flask_jwt_extended import create_access_token
from pytest_mock import mocker
from datetime import datetime, timezone, timedelta
from freezegun import freeze_time
import pytest
from flask_wtf.csrf import generate_csrf


@pytest.mark.parametrize(
    "data, expected_status, message",
    [
        (
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "testpassword",
                "passwordRepeat": "testpassword",
            },
            201,
            b"Successfully registered.",
        ),
        (
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "testpassword",
                "passwordRepeat": "differentpassword",
            },
            202,
            b"Passwords do not match",
        ),
        (
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "tes",
                "passwordRepeat": "tes",
            },
            202,
            b"Password must be >=4 characters long",
        ),
        (
            {
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "testpassword",
            },
            202,
            b"Missing data",
        ),
    ],
)
def test_registartion(client, data, expected_status, message):
    response = client.post("/registration", json=data)
    assert response.status_code == expected_status
    assert message in response.data


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


@pytest.mark.parametrize(
    "data, expected_status, message",
    [
        (
            {
                "username": "testuser",
                "password": "testpassword",
            },
            200,
            b'"login":true',
        ),
        (
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
            200,
            b"Incorrect Password.",
        ),
        (
            {
                "username": "testuser",
            },
            201,
            b"Missing data.",
        ),
        (
            {
                "username": "no_user",
                "password": "testpassword",
            },
            200,
            b"Account does not exist.",
        ),
    ],
)
def test_login(app, client, data, expected_status, message):
    with app.app_context():
        account = Account(username="testuser", email="testuser@test.com")
        account.set_password("testpassword")
        db.session.add(account)
        db.session.commit()

        response = client.post("/login", json=data)

        assert message in response.data
        assert response.status_code == expected_status


def test_login_use_POST(client):
    response = client.get(
        "/login", json={"username": "testuser", "password": "password"}
    )

    assert response.status_code == 201
    assert b"Use POST" in response.data


def test_logout(app, client, new_account):
    with app.app_context():
        db.session.add(new_account)
        db.session.commit()
        token = create_access_token(identity=new_account.id)
        client.set_cookie("localhost", "access_token_cookie", token)
        response = client.post("/logout")
        assert b'"logout":true' in response.data


def test_show_account_no_account(app, client, new_account):
    with app.app_context():
        token = create_access_token(identity=new_account.id)
        client.set_cookie("localhost", "access_token_cookie", token)
        response = client.get("/profile")
        assert b"Account does not exist." in response.data


def test_show_account_token_expired(app, client, new_account):
    with app.app_context():
        expires_delta = timedelta(seconds=1)
        token = create_access_token(
            identity=new_account.id, expires_delta=expires_delta
        )
        expired_timestamp = datetime.fromtimestamp(
            datetime.timestamp(datetime.now(timezone.utc)) + 2, timezone.utc
        )

        with freeze_time(expired_timestamp):
            client.set_cookie("localhost", "access_token_cookie", token)

            response = client.get("/profile")

            assert response.status_code == 401
            assert b"Token has expired" in response.data


def test_show_account_success(app, client, new_account):
    with app.app_context():
        db.session.add(new_account)
        db.session.commit()
        token = create_access_token(identity=new_account.id)
        client.set_cookie("localhost", "access_token_cookie", token)

        response = client.get("/profile")

        assert str(new_account.id) in str(response.data)
        assert str(new_account.email) in str(response.data)
        assert str(new_account.username) in str(response.data)


def test_newgame_auth(client, app, new_account):
    with app.app_context():
        db.session.add(new_account)
        db.session.commit()
        token = create_access_token(identity=new_account.id)
        client.set_cookie("localhost", "access_token_cookie", token)

        response = client.get("/creategame")
        id = response.get_json().get("id")

        assert bytes('"id":"%s"' % id, "utf-8") in response.data

