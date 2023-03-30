from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from datetime import datetime
import jwt
from config import Config

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    username = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(256), nullable=False)
    created_on = db.Column(postgresql.TIMESTAMP(), autoincrement=False)
    last_login = db.Column(postgresql.TIMESTAMP(), autoincrement=False,
                           nullable=True)
    
    def encode_auth_token(self, id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': id
            }
            return jwt.encode(
                payload,
                Config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, Config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'


class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.INTEGER(), autoincrement=True, nullable=False,
                   primary_key=True)
    player_id = db.Column(db.INTEGER(), db.ForeignKey('account.id'),
                          autoincrement=False, nullable=False)
    game_id = db.Column(db.INTEGER(), db.ForeignKey('game.id'),
                        autoincrement=False, nullable=False)

    player_game_id_fkey = db.relationship('Game', foreign_keys='Player.game_id')
    player_player_id_fkey = db.relationship('Account', foreign_keys='Player.player_id')


class Result(db.Model):
    __tablename__ = "result"
    id = db.Column(db.INTEGER(), autoincrement=True, nullable=False, primary_key=True)
    description = db.Column(db.VARCHAR(length=128), autoincrement=False, nullable=True)
    postgresql_ignore_search_path = False


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True,
                   nullable=False)
    start_time = db.Column(db.TIMESTAMP(), autoincrement=False,
                           nullable=False)
    end_time = db.Column(db.TIMESTAMP(), autoincrement=False,
                         nullable=True)
    player_one_id = db.Column(db.INTEGER(), db.ForeignKey('account.id'),
                              autoincrement=False, nullable=False)
    player_two_id = db.Column(db.INTEGER(), db.ForeignKey('account.id'),
                              autoincrement=False, nullable=False)
    result_id = db.Column(db.INTEGER(), db.ForeignKey('result.id'),
                          autoincrement=False, nullable=True)

    game_result_id_fkey = db.relationship('Result',
                                          foreign_keys='Game.result_id')
    game_player_one_id_fkey = db.relationship('Account',
                                              foreign_keys='Game.player_one_id')
    game_player_two_id_fkey = db.relationship('Account',
                                              foreign_keys='Game.player_two_id')
