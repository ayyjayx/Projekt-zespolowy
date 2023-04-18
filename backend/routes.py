from datetime import datetime, timedelta
import jwt
from config import Config
from flask import jsonify, make_response, request
from models import Account, db, JWTTokenBlocklist
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt, set_access_cookies, unset_jwt_cookies, create_refresh_token
from flask_cors import cross_origin
from datetime import datetime, timedelta, timezone


def init_routes(app):
        
    @app.route("/loggedhome", methods=["GET", "POST"])
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
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response("Missing data.", 200)

            account = Account.query.filter_by(username=username).first()

            if not account:
                return make_response("Account does not exist.", 200)

            if account.check_password(password):
                access_token = create_access_token(identity=account.id)
                refresh_token = create_refresh_token(identity=account.id)
                response = jsonify(access_token=access_token, refresh_token=refresh_token)
                response.headers['Access-Control-Allow-Methods']='http://localhost:3000'
                return response

            return make_response("Incorrect Password.", 200)
        else:
            return make_response("Use POST", 200)
    
    @app.route("/logout", methods=["GET", "POST"])
    @jwt_required()
    def logout():
        token = request.headers["Authorization"]

        jwt_block = JWTTokenBlocklist(jwt_token=token)
        jwt_block.save()
        response = make_response("Token expired.", 200)
        unset_jwt_cookies(response)
        return response
        
    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def show_account():
        # data = request.get_json()
        # id = data.get("id")
        # account = Account.query.get(id)
        current_user = get_jwt_identity()
        print("current user", current_user)
        account = Account.query.get(current_user)
        print("account", account)
        
        exp_timestamp = get_jwt()["exp"]
        if datetime.now(timezone.utc) > exp_timestamp:
            return make_response("Access token expired", 210)

        if not account:
            return make_response("Account does not exist.", 404)
            
        
        return jsonify({
            "id": account.id,
            "email": account.email,
            "username": account.username,
            "created_on": account.created_on}), 200

    @app.route("/profile/update", methods=["GET", "POST"])
    @jwt_required()
    @cross_origin()
    def edit_account():
        data = request.get_json()
        id = data.get('id')
        payload = data.get("updatePayload")
        id = payload.get("id")
        new_username = payload.get("username")
        new_email = payload.get("email")
        password = payload.get("password")
        account = Account.query.filter_by(id=id).first()
        
        exp_timestamp = get_jwt()["exp"]
        if datetime.now(timezone.utc) > exp_timestamp:
            return make_response("Access token expired", 210)

        if not account:
            return make_response("Account does not exist", 201)

        if request.method == 'POST':
            new_username = payload.get("username")
            new_email = payload.get("email")
            password = payload.get("password")
            
            if account.check_password(password):
                if new_username != '':
                    account.update_username(new_username)

                if new_email != '':
                    account.update_email(new_email)

                account.save()
                return make_response("Account successfully updated.", 200)

            return make_response("Wrong password.", 201)

        return jsonify({
            "id": account.id,
            "email": account.email,
            "username": account.username}), 201

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
    
    @app.route("/refresh", methods=["POST"])
    @jwt_required()
    def refresh():
        dane = request.headers["Authorization"]
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        access_token = create_access_token(identity=account.id)
        response = jsonify(access_token=access_token)
        return response