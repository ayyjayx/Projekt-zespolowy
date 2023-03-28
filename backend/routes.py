from flask import request, session, jsonify, render_template, url_for, redirect, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
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
        post_data = request.get_json()
        new_account = Account.query.filter_by(username=post_data.get('username')).first()
        if not new_account:
            try:
                new_account = Account(
                    username=post_data.get('username'),
                    email=post_data.get('email'),
                    password=generate_password_hash(post_data.get('password'))
                )
                db.session.add(new_account)
                db.session.commit()
                auth_token = new_account.encode_auth_token(new_account.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists.',
            }
            return make_response(jsonify(responseObject)), 202

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        post_data = request.get_json()
        try:
            account = Account.query.filter_by(username=post_data.get('username')).first()
            if check_password_hash(account.password, post_data.get('password')):
                auth_token = account.encode_auth_token(account.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again.'
            }
            return make_response(jsonify(responseObject)), 500  

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        # logout
        return redirect(url_for('start'))

