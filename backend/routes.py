from datetime import datetime, timedelta
import jwt
from config import Config
from flask import (jsonify, make_response, redirect, render_template,
                   request, session, url_for)
from models import Account, db, token_required, admin_token_required
from werkzeug.security import check_password_hash, generate_password_hash
# from flask_jwt_extended import decode_token, get_jwt, jwt_required

def init_routes(app):
    @app.route("/api", methods=["GET", "POST"])
    def api():
        data = request.get_data()
        return jsonify(data)

    @app.route("/index", methods=["GET"])
    def index():
        return render_template("index.html")

    # @app.route('/get-username')
    # @token_required
    # def get_username(current_user):
    #     return jsonify({"username": current_user.username})

    @app.route("/registration", methods=["GET", "POST"])
    def registration():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            passwordRepeat = data.get("passwordRepeat")

            if password == passwordRepeat:
                account = Account.query.filter_by(email=email).first()
                if not account:
                    new_account = Account(
                        username=username,
                        email=email,
                        password=generate_password_hash(password),
                    )
                    db.session.add(new_account)
                    db.session.commit()
                    return make_response("Successfully registered.", 201)
                else:
                    return make_response("User already exists.", 202)
            else: return make_response("Passwords do not match", 202)
        else: return make_response("Use POST", 200)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                responseObject = {"status": "fail", "message": "Missing data!"}
                return make_response(jsonify(responseObject), 401)

            account = Account.query.filter_by(username=username).first()
            if not account:
                responseObject = {"status": "fail", "message": "User does not exist!"}
                return make_response(jsonify(responseObject), 401)

            if check_password_hash(account.password, password):
                token = jwt.encode(
                    {"id": account.id, "username": account.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
                    app.config["SECRET_KEY"],
                )
                return jsonify({"token": token})

            responseObject = {"status": "fail", "message": "Incorrect Password!"}
            return make_response(jsonify(responseObject), 403)
        else: return make_response("Use POST", 200)

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        # logout
        return redirect(url_for("start"))
    
    @app.route("/admin/accounts", methods=["GET", "POST"])
    @admin_token_required
    def admin():
        return jsonify({"admin": 'admins page'})
