from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash

class Account(db.Model):
    __tablename__='account'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    def __repr__(self):
        return '<Account {}>'.format(self.email)
