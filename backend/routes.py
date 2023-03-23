from flask import jsonify, request
from models import db, account
from sqlalchemy import exc
# from flask_login import LoginManager, login_user
# from datetime import datetime


def init_routes(app):

    @app.route("/api", methods=["GET"])
    def get_api_base_url():
        return jsonify({
            "msg": "todos api is up",
            "success": True,
            "data": None
        }), 200

    @app.route("/register", methods=["POST"])
    def register():
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        if username and email and password:
            try:
                new_user = account(
                    username=username,
                    email=email,
                    password=password
                )
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'success': True}), 201
            except exc.IntegrityError:
                return jsonify({'error':
                                'użytkownik/email są już używane'}), 400
        else:
            return jsonify({'error': 'uzupełnij wszystkie pola'}), 400

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # login_manager = LoginManager(app)
        username = request.json.get('username')
        password = request.json.get('password')

        acc = account.query.filter_by(username=username).first()

        if acc:
            if acc.password == password:
                # login_user(account)
                return jsonify({'message': 'Udane logowanie'}), 200
            else:
                return jsonify({'error': 'Złe hasło'}), 401
        else:
            return jsonify({'error': 'Nie znaleziono użytkownika'}), 401
