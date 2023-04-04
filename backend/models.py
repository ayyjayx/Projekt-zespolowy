from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from functools import wraps
from flask import request, jsonify
import jwt
import app

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    username = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(256), nullable=False)
    created_on = db.Column(postgresql.TIMESTAMP(), autoincrement=False)
    last_login = db.Column(postgresql.TIMESTAMP(), autoincrement=False, nullable=True)
    admin = db.Column(db.Boolean, default=False)


class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.INTEGER(), autoincrement=True, nullable=False, primary_key=True)
    player_id = db.Column(
        db.INTEGER(), db.ForeignKey("account.id"), autoincrement=False, nullable=False
    )
    game_id = db.Column(
        db.INTEGER(), db.ForeignKey("game.id"), autoincrement=False, nullable=False
    )

    player_game_id_fkey = db.relationship("Game", foreign_keys="Player.game_id")
    player_player_id_fkey = db.relationship("Account", foreign_keys="Player.player_id")


class Result(db.Model):
    __tablename__ = "result"
    id = db.Column(db.INTEGER(), autoincrement=True, nullable=False, primary_key=True)
    description = db.Column(db.VARCHAR(length=128), autoincrement=False, nullable=True)
    postgresql_ignore_search_path = False


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True, nullable=False)
    start_time = db.Column(db.TIMESTAMP(), autoincrement=False, nullable=False)
    end_time = db.Column(db.TIMESTAMP(), autoincrement=False, nullable=True)
    player_one_id = db.Column(
        db.INTEGER(), db.ForeignKey("account.id"), autoincrement=False, nullable=False
    )
    player_two_id = db.Column(
        db.INTEGER(), db.ForeignKey("account.id"), autoincrement=False, nullable=False
    )
    result_id = db.Column(
        db.INTEGER(), db.ForeignKey("result.id"), autoincrement=False, nullable=True
    )

    game_result_id_fkey = db.relationship("Result", foreign_keys="Game.result_id")
    game_player_one_id_fkey = db.relationship(
        "Account", foreign_keys="Game.player_one_id"
    )
    game_player_two_id_fkey = db.relationship(
        "Account", foreign_keys="Game.player_two_id"
    )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = Account.query.filter_by(id=data["id"]).first()
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        current_user.username = data["username"]
        
        return f(current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401
        
        admin = token.get('admin')

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = Account.query.filter_by(id=data["id"]).first()
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
