from flask import request, session, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from models import db, Account
from sqlalchemy import exc
from datetime import datetime


def init_routes(app):

    @app.route('/start', methods=['GET'])
    def start():
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

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            hashed = generate_password_hash(password)
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
            return redirect(url_for('start'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            account = Account.query.filter_by(username=form.username.data).first()
            if account:
                if check_password_hash(account.password, form.password.data):
                    session['logged_in'] = True
                    flash('Successful Login :)', 'success')
                    return redirect(url_for('start'))
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
        flash('Successfully Logged out', 'success')
        return redirect(url_for('start'))

    @app.route('/admin/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'GET':
            return render_template('create.html')
        if request.method == 'POST':
            form = RegistrationForm()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            hashed = generate_password_hash(password)
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
                return redirect(url_for('/admin/create'))
