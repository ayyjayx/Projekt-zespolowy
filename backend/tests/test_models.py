import pytest
from models import Account, ResetToken, Game


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

        new_email = "newemail@test.py"
        new_username = "newusername"
        new_password = "newpassword"

        account.update_email(new_email)
        account.update_username(new_username)
        account.update_password(new_password)

        assert account.email == new_email
        assert account.username == new_username
        assert account.password != new_password
        assert str(account) == f"User {account.username}"

        account.delete()

        account = Account.query.filter_by(email=new_email).first()

        assert account is None


def test_token(new_token, app):
    with app.app_context():
        new_token.save()
        token = ResetToken.query.filter_by(username="testuser").first()

        assert token is not None

        token.delete()
        token = ResetToken.query.filter_by(username="testuser").first()

        assert token is None


def test_game(new_game, app):
    with app.app_context():
        new_game.save()
        game = Game.query.filter_by(id=1).first()

        new_fen = "other_fen"
        outcome = "BLACK WIN"
        game.update_fen(new_fen)
        game.set_end_time()
        game.set_result(outcome)
        game_dict = game.to_dict()

        assert game is not None
        assert game.fen == new_fen
        assert game.end_time is not None
        assert game.result == outcome
        assert game.id in game_dict.values()
        assert game.start_time.strftime("%H:%M %d %B %Y") in game_dict.values()
        assert game.end_time.strftime("%H:%M %d %B %Y") in game_dict.values()
        assert game.fen in game_dict.values()
        assert game.result in game_dict.values()

        game.delete()
        game = Game.query.filter_by(id=1).first()

        assert game is None
