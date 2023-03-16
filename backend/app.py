from flask import Flask, request, flash, redirect, url_for
import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
from models import Account

app = Flask(__name__)

engine = db.create_engine('postgresql+psycopg2://postgres:projekt1234@database:5432/postgres')
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def main():
    # test - bez POST request
    # meta = db.MetaData()
    # census = db.Table('account', meta, autoload_with=engine)
    # return(census.columns.keys())
    return "szachy"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_account = Account(username=username, password=password, email=email)
        session.add(user_account)
        session.commit()
        flash('Udana rejestracja')
        return redirect(url_for('main'))
    return 'no POST request :)'

if __name__ == '__main__':
    app.run(debug=True)