from flask import jsonify, request, session, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from models import db, Account
from sqlalchemy import exc
from datetime import datetime


def init_routes(app):

    @app.route('/', methods=['GET'])
    def main():
        if session.get('logged_in'):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('index'))
        
    @app.route('/home', methods=['GET'])
    def home():
        return render_template('home.html')

    @app.route('/index', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route("/register", methods=["POST"])
    def register():
        if request.method == 'POST':
            form = RegistrationForm()
            if form.validate_on_submit():
                username = form.username.data
                email = form.email.data
                password = form.password.data
                hashed = generate_password_hash(password, method='sha256')
                    try:
                        new_user = Account(
                            username=username,
                            email=email,
                            password=hashed,
                            created_on=datetime.utcnow())
                        db.session.add(new_user)
                        db.session.commit()
                    except exc.IntegrityError:
                        flash('Username/Email already in use!', 'error')
                        return redirect(url_for('register'))
                    session['logged_in'] = True
                    flash('Successful Registration :)', 'success')
                    return redirect(url_for('/'))
            else:
                flash('Fill missing fields!', 'error')
                return redirect(url_for('register'))
        else: return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            account = Account.query.get(form.username.data)
            if account:
                if check_password_hash(account.password, form.password.data):
                    session['logged_in'] = True
                    flash('Successful Login :)', 'success')
                    return redirect(url_for('/')) 
                else:
                    flash('Wrong Password!', 'error')
                    return redirect(url_for('login'))
            else:
                flash('Account does not exist!', 'error')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)
        
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session['logged_in'] = False
        flash('Successfuly Logged out', 'success')
        return redirect(url_for('/'))
