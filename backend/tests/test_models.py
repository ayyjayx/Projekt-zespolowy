import pytest
from models import Account

@pytest.fixture
def new_account():
    account = Account(
        email="pytest@test.com",
        username="testuser",
        password="password",
        admin=False
    )
    return account

def test_account(new_account):
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