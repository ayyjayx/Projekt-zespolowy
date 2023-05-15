import pytest
from models import Account


def test_account(new_account, app):
    with app.app_context():
        new_account.save()

        # add new account to database, check is it exists
        account = Account.query.filter_by(email="pytest@test.com").first()
        assert account is not None

        # check if all data is as input
        assert account.email == "pytest@test.com"
        assert account.username == "testuser"
        assert account.admin == False

        # check password hash
        assert account.password != "password"
