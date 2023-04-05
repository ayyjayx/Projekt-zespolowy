from datetime import datetime, timedelta
import jwt
from config import Config
from flask import jsonify, make_response, request
from models import Account, db, JWTTokenBlocklist
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


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
                token = create_access_token(identity=account.id)
                return jsonify({"token": token})

            return make_response("Incorrect Password.", 403)
        else:
            return make_response("Use POST", 200)

    @app.route("/logout", methods=["GET", "POST"])
    @jwt_required()
    def logout():
        token = request.headers["Authorization"]

        jwt_block = JWTTokenBlocklist(jwt_token=token)
        jwt_block.save()

        return make_response("Token expired.", 200)
        
    @app.route("/account", methods=["GET"])
    @jwt_required()
    def show_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)

        if not account:
            return make_response("Account does not exist.", 404)
        
        return jsonify({
            "id": account.id,
            "email": account.email,
            "username": account.username,
            "created_on": account.created_on}), 200

    @app.route("/account/update", methods=["GET", "POST"])
    @jwt_required()
    def edit_account():
        data = request.get_json()
        id = data.get("id")
        account = Account.query.filter_by(id=id).first()

        if not account:
            return make_response("Account does not exist", 404)

        if request.method == 'POST':
            data = request.get_json()
            new_username = data.get("username")
            new_email = data.get("email")
            new_password = data.get("password")
            new_passwordRepeat = data.get("passwordRepeat")

            if new_username is not None:
                account.update_username(new_username)

            if new_email is not None:
                account.update_email(new_email)

            if new_password is not None and new_passwordRepeat is not None:
                if new_password == new_passwordRepeat:
                    account.update_password(new_password)

            account.save()

            return make_response("Account successfully updated.", 200)

        return jsonify({
            "id": account.id,
            "email": account.email,
            "username": account.username}), 200

    @app.route("/account/delete", methods=["DELETE"])
    @jwt_required()
    def delete_account():
        data = request.get_json()
        id = data.get("id")
        account = Account.query.filter_by(id=id).first()

        if not account:
            return make_response("Account does not exist", 404)
        
        account.delete()

        return make_response("Account successfully deleted.", 200)
