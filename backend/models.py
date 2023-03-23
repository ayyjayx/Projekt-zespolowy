from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

db = SQLAlchemy()


class account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    # created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Account {self.id}, {self.username}>"
