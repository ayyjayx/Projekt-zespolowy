from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class ResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, username, token):
        self.username = username
        self.token = token

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    admin = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    def update_username(self, new_username):
        self.username = new_username

    def update_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Player(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    player_id = db.Column(db.Integer(), db.ForeignKey("account.id"), nullable=False)
    game_id = db.Column(db.Integer(), db.ForeignKey("game.id"), nullable=False)

    player_game_id_fkey = db.relationship("Game", foreign_keys="Player.game_id")
    player_player_id_fkey = db.relationship("Account", foreign_keys="Player.player_id")


class Result(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    description = db.Column(db.String(128), nullable=True)
    postgresql_ignore_search_path = False


class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=True)
    player_one_id = db.Column(db.Integer(), db.ForeignKey("account.id"), nullable=False)
    player_two_id = db.Column(db.Integer(), db.ForeignKey("account.id"), nullable=False)
    result_id = db.Column(db.Integer(), db.ForeignKey("result.id"), nullable=True)

    game_result_id_fkey = db.relationship("Result", foreign_keys="Game.result_id")
    game_player_one_id_fkey = db.relationship(
        "Account", foreign_keys="Game.player_one_id"
    )
    game_player_two_id_fkey = db.relationship(
        "Account", foreign_keys="Game.player_two_id"
    )
