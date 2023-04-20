from flask import jsonify, make_response, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required,
                                unset_jwt_cookies)
from models import Account

def init(app):
    @app.route("/loggedhome", methods=["GET", "POST"])
    def home():
        data = request.get_data()
        return jsonify(data)

    @app.route("/registration", methods=["GET", "POST"])
    def registration():
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            passwordRepeat = data.get("passwordRepeat")

            if not username or not password or not email or not passwordRepeat:
                return make_response("Missing data.", 202)

            if len(password) < 4:
                return make_response("Password must be at least 4 characters long.", 202)

            if password == passwordRepeat:
                username_exists = Account.query.filter_by(username=username).first()
                email_exists = Account.query.filter_by(email=email).first()
                if not username_exists:
                    if not email_exists:
                        new_account = Account(username=username, email=email)
                        new_account.set_password(password)
                        new_account.save()
                        return make_response(
                            "Successfully registered new user. Proceed to Log in.", 201
                        )
                    else:
                        return make_response(
                            "Email already in use.", 202
                        )
                else:
                    return make_response("Username already in use.", 202)
            else:
                return make_response("Passwords do not match.", 202)
        else:
            return make_response("Use POST method.", 200)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response("Missing data.", 201)

            account = Account.query.filter_by(username=username).first()

            if not account:
                return make_response("User does not exist.", 201)

            if account.check_password(password):
                access_token = create_access_token(identity=account.id)
                refresh_token = create_refresh_token(identity=account.id)
                response = jsonify(
                    access_token=access_token, refresh_token=refresh_token
                )
                return response

            return make_response("Wrong password.", 201)
        else:
            return make_response("Use POST", 201)

    @app.route("/logout", methods=["GET", "POST"])
    @jwt_required()
    def logout():
        response = make_response("Token expired.", 200)
        unset_jwt_cookies(response)
        return response
    
    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        dane = request.headers["Authorization"]
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        access_token = create_access_token(identity=account.id)
        response = jsonify(access_token=access_token)
        return response
    
    