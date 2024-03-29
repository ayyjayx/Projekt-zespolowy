from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableList

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
    

class Game(db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime(), nullable=True, default=None)
    fen = db.Column(db.String(), nullable=False)
    player_one_id = db.Column(db.Integer(), nullable=False)
    player_two_id = db.Column(db.Integer(), nullable=True)
    result = db.Column(db.String(), nullable=True, default=None)
    moves = db.Column(MutableList.as_mutable(postgresql.ARRAY(db.String())), default=[], nullable=True)
    
    def set_player_black(self, player):
        self.player_two_id = player

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_fen(self, new_fen):
        self.fen = new_fen

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_end_time(self):
        self.end_time=datetime.utcnow()

    def set_result(self, outcome):
        self.result = outcome

    def add_move(self, move):
        self.moves.append(move)

    def to_dict(self):
        return {
            'id': self.id,
            'start_time': self.start_time.strftime("%H:%M %d %B %Y"),
            'end_time': self.end_time,
            'fen': self.fen,
            'result': self.result,
            'san': ','.join(self.moves) if self.moves else []
        }
