from datetime import datetime, timezone, timedelta

from config import Config
from flask import jsonify, make_response, render_template_string, request
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required,
                                unset_jwt_cookies)
from flask_mail import Mail, Message
from models import Account, ResetToken


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
                return make_response("Missing data", 202)

            if len(password) < 4:
                return make_response("Password must be >=4 characters long", 202)

            if password == passwordRepeat:
                username_exists = Account.query.filter_by(username=username).first()
                email_exists = Account.query.filter_by(email=email).first()
                if not username_exists:
                    if not email_exists:
                        new_account = Account(username=username, email=email)
                        new_account.set_password(password)
                        new_account.save()
                        return make_response(
                            "Successfully registered.", 201
                        )
                    else:
                        return make_response(
                            "Ten email jest już przypisany do konta", 202
                        )
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
                return make_response("Missing data.", 201)

            account = Account.query.filter_by(username=username).first()

            if not account:
                return make_response("Account does not exist.", 200)

            if account.check_password(password):
                access_token = create_access_token(identity=account.id)
                refresh_token = create_refresh_token(identity=account.id)
                response = jsonify(
                    access_token=access_token, refresh_token=refresh_token
                )
                return response

            return make_response("Incorrect Password.", 200)
        else:
            return make_response("Use POST", 201)

    @app.route("/logout", methods=["GET", "POST"])
    @jwt_required()
    def logout():
        response = make_response("Token expired.", 200)
        unset_jwt_cookies(response)
        return response

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def show_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        exp_timestamp = get_jwt()["exp"]
        now_timestamp = datetime.timestamp(datetime.now(timezone.utc))

        if now_timestamp > exp_timestamp:
            return make_response("Access token expired", 200)
        
        if not account:
            return make_response("Account does not exist.", 404)

        return (
            jsonify(
                {
                    "id": account.id,
                    "email": account.email,
                    "username": account.username,
                    "created_on": account.created_on,
                }
            ),
            200,
        )

    @app.route("/profile/update", methods=["GET", "POST"])
    @jwt_required()
    @cross_origin()
    def edit_account():
        data = request.get_json()
        exp_timestamp = get_jwt()["exp"]
        now_timestamp = datetime.timestamp(datetime.now(timezone.utc))
        if now_timestamp > exp_timestamp:
            return make_response("Access token expired", 200)

        id = data.get("id")
        payload = data.get("updatePayload")
        id = payload.get("id")
        new_username = payload.get("username")
        new_email = payload.get("email")
        password = payload.get("password")
        account = Account.query.filter_by(id=id).first()

        if not account:
            return make_response("Użytkownik nie istnieje.", 201)

        if request.method == "POST":
            new_username = payload.get("username")
            new_email = payload.get("email")
            password = payload.get("password")

            if account.check_password(password):
                if new_username != "":
                    username_exists = Account.query.get(username=new_username)
                    if not username_exists:
                        account.update_username(new_username)

                if new_email != "":
                    email_exists = Account.query.get(username=new_email)
                    if not email_exists:
                        account.update_email(new_email)

                account.save()
                return make_response("Dane konta zaktualizowane", 200)

            return make_response("Niepoprawne hasło.", 201)

        return (
            jsonify(
                {"id": account.id, "email": account.email, "username": account.username}
            ),
            201,
        )

    @app.route("/profile/delete", methods=["DELETE"])
    @jwt_required()
    def delete_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        if not account:
            return make_response("Account does not exist", 404)

        account.delete()

        return make_response("Account successfully deleted.", 200)

    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        dane = request.headers["Authorization"]
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        access_token = create_access_token(identity=account.id)
        response = jsonify(access_token=access_token)
        return response

    @app.route("/reset_send_email", methods=["GET", "POST"])
    def reset():
        try:
            data = request.get_json()
            email = data.get("email")
            account = Account.query.filter_by(email=email).first()

            reset_token = create_access_token(identity=account.id)
            newResetToken = ResetToken(username=account.username, token=reset_token)
            newResetToken.save()

            with app.app_context():
                mail = Mail(app)
                msg = Message()
                msg.subject = "Szaszki Password Reset"
                msg.sender = Config.MAIL_USERNAME
                msg.recipients = [email]
                msg.html = render_template_string(
                    """
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Zapomniane Hasło - Szaszki</title>
                        </head>
                        <body>
                            <h1>Resetowanie Hasła</h1>
                            <p>Drogi Użytkowniku {{ account }},</p>
                            <p>Dostaliśmy zapytanie o reset hasła. Jeśli nie jesteś właścicielem konta, zignoruj ten email.</p>
                            <p>Żeby zresetować hasło kliknij w poniższy link:</p>
                            <p><a href="http://localhost:3000/reset_password?token={{token}}&email={{email}}">Resetuj Hasło</a></p>
                            <p>Link będzie aktywny przez 1h</p>
                            <p>have fun baby,</p>
                            <p>The Szaszki Team</p>
                        </body>
                        </html>
                    """,
                    account=account.username,
                    token=reset_token,
                    email=email
                )
                mail.send(msg)

            return make_response("Email has been sent.", 201)
        except:
            return make_response("Could not send email.", 230)

    @app.route("/reset_password", methods=["GET", "POST"])
    @cross_origin()
    def reset_password():
        token = None

        if request.method == "GET":
            token = request.args.get("token")
            email = request.args.get("email")
            return jsonify({"msg": "successfully got url params."})

        else:
            data = request.get_json()
            token = data.get('token')
            email = data.get('email')
            
            reset_token = ResetToken.query.filter_by(token=token).first()

            expiration_time = timedelta(hours=1)
            current_time = datetime.utcnow()

            if reset_token:
                reset_token.delete()
            else:
                return jsonify({"msg": "Access to reset link has expired."})
            
            if current_time - reset_token.created_at > expiration_time:
                reset_token.delete()
                return jsonify({"msg": "Reset token has expired."})
            
            account = Account.query.filter_by(email=email).first()
            if not account:
                return jsonify({"msg": "User does not exist."})

            new_password = data.get("password")
            new_passwordR = data.get("passwordRepeat")

            if not new_password or not new_passwordR:
                return jsonify({"msg": "Missing data."})

            if len(new_password) < 4:
                return jsonify({"msg": "Password must be at least 4 characters long."})

            if new_password == new_passwordR:
                account.update_password(new_password)
                account.save()
                return jsonify({"msg": "Password successfully updated."})

            else:
                return jsonify({"msg": "Passwords do not match."})