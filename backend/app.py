from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/account'
db.init_app(app)

@app.route('/')
def main():
    return "szachy"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = Account(username=username, password=password, email=email)
        db.session.add(account)
        db.session.commit()
        return 'Udana rejestracja'
    return 'Aktywne'

if __name__ == '__main__':
    app.run(debug=True)
