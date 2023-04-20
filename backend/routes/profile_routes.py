from datetime import datetime, timezone, timedelta

from config import Config
from flask import jsonify, make_response, render_template_string, request
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                jwt_required)
from flask_mail import Mail, Message
from models import Account, ResetToken

def init(app):
    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def show_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        exp_timestamp = get_jwt()["exp"]
        now_timestamp = datetime.timestamp(datetime.now(timezone.utc))

        if now_timestamp > exp_timestamp:
            return make_response("Access token expired.", 200)
        
        if not account:
            return make_response("User does not exist.", 404)

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
        payload = data.get("updatePayload")
        id = payload.get("id")
        new_username = payload.get("username")
        new_email = payload.get("email")
        password = payload.get("password")
        account = Account.query.filter_by(id=id).first()

        if not account:
            return make_response("User does not exist.", 201)

        if request.method == "POST":
            new_username = payload.get("username")
            new_email = payload.get("email")
            password = payload.get("password")

            if account.check_password(password):
                if new_username != "":
                    username_exists = Account.query.filter_by(username=new_username).first()
                    if not username_exists:
                        account.update_username(new_username)

                if new_email != "":
                    email_exists = Account.query.filter_by(email=new_email).first()
                    if not email_exists:
                        account.update_email(new_email)

                account.save()
                return make_response("User data successfully updated.", 200)

            return make_response("Wrong password.", 201)

        return (
            jsonify(
                {"id": account.id, "email": account.email, "username": account.username}
            ),
            201,
        )

    @app.route("/profile/update/password", methods=["GET", "POST"])
    @jwt_required()
    def update_password():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        data = request.get_json()
        password = data.get("password")
        new_password = data.get("newPassword")
        new_password_repeat = data.get("newPasswordRepeat")

        if not account:
            return make_response("User does not exist.", 201)
        
        if account.check_password(password):
            if len(new_password) < 4:
                return make_response("Password must be at least 4 characters long.", 202)
            
            if new_password == new_password_repeat:
                account.update_password(new_password)
                account.save()
                return make_response("User password successfully updated.", 200)
            else:
                return make_response("Passwords do not match.", 201)
        else:
            return make_response("Wrong current password.", 201)

    @app.route("/profile/delete", methods=["DELETE"])
    @jwt_required()
    def delete_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        if not account:
            return make_response("User does not exist.", 404)

        account.delete()

        return make_response("User successfully deleted.", 200)

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

