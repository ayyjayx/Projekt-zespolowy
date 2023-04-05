from datetime import datetime, timedelta
import jwt
from config import Config
from flask import jsonify, make_response, request
from models import Account, db, JWTTokenBlocklist
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return jsonify({"message": "Token is missing !!"}), 400

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = Account.query.filter_by(id=data["id"]).first()

            if not current_user:
                return jsonify({"message": "Account does not exist."}), 400

            token_expired = db.session.query(JWTTokenBlocklist.id)\
                .filter_by(jwt_token=token).scalar()

            if token_expired is not None:
                return jsonify({"message": "Token expired."}), 400

            if not current_user.check_jwt():
                return jsonify({"message": "Token expired."}), 400

        except:
            return jsonify({"message": "Token is invalid."}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def init_routes(app):
    @app.route("/home", methods=["GET", "POST"])
    def home():
        data = request.get_data()
        return jsonify(data)

    @app.route("/registration", methods=["GET", "POST"])
    def registration():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            passwordRepeat = data.get("passwordRepeat")

            if not username or not password or not email or not passwordRepeat:
                return make_response("Missing data", 401)

            if len(password) < 4:
                return make_response("Password must be >=4 characters long", 411)

            if password == passwordRepeat:
                account_exists = Account.query.filter_by(email=email).first()
                if not account_exists:
                    new_account = Account(
                        username=username,
                        email=email
                    )
                    new_account.set_password(password)
                    new_account.save()

                    return make_response("Successfully registered.", 201)
                else:
                    return make_response("Account already exists.", 202)
            else:
                return make_response("Passwords do not match", 202)
        else:
            return make_response("Use POST method", 200)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response("Missing data.", 401)

            account = Account.query.filter_by(username=username).first()

            if not account:
                return make_response("Account does not exist.", 401)

            if account.check_password(password):
                token = jwt.encode({
                    "id": account.id,
                    "username": account.username,
                    "admin": account.admin,
                    "exp": datetime.utcnow() + timedelta(minutes=30)},
                    Config.SECRET_KEY
                )
                return jsonify({"token": token}), 300

            return make_response("Incorrect Password.", 403)
        else:
            return make_response("Use POST", 200)

    @app.route("/logout", methods=["GET", "POST"])
    @token_required
    def logout():
        token = request.headers["Authorization"]

        jwt_block = JWTTokenBlocklist(jwt_token=token)
        jwt_block.save()

        return make_response("Token expired.", 200)

    @app.route("/admin/accounts/edit/<int:account_id>", methods=["GET", "POST"])
    @token_required
    def edit_account(account_id):
        account = Account.query.filter_by(id=account_id).first()

        if not account:
            return make_response("Account does not exist", 404)

        if request.method == 'POST':
            data = request.get_json()
            new_username = data.get("username")
            new_email = data.get("email")

            account.update_email(new_email)
            account.update_username(new_username)
            account.save()

            return make_response("Account successfully updated.", 200)

        return jsonify({
            "id": account.id,
            "email": account.email,
            "username": account.username}), 200
