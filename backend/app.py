from flask import Flask, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:projekt1234@localhost:80/account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

class Account(db.Model):
    __tablename__='account'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

@app.route('/')
def main():
    return "szachy"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_account = Account(username=username, password=password, email=email)
        db.session.add(user_account)
        db.session.commit()
        flash('Udana rejestracja')
        return redirect(url_for('main'))
    return 'no POST request :)'

if __name__ == '__main__':
    app.run(debug=True)
