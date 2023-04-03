from datetime import datetime, timedelta

import app
import jwt
from config import Config
from flask import (flash, jsonify, make_response, redirect, render_template,
                   request, session, url_for)
from models import Account, db, token_required
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash


def init_routes(app):
    @app.route("/start", methods=["GET"])
    def start():
        if session.get("logged_in"):
            return redirect(url_for("home"))
        else:
            return redirect(url_for("index"))

    @app.route("/home", methods=["GET"])
    def home():
        return render_template("home.html")

    @app.route("/index", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/registration", methods=["GET", "POST"])
    def registration():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            passwordRepeat = data.get("passwordRepeat")

            if not username or not password or not email or not passwordRepeat:
                responseObject = {"status": "fail", "message": "Missing data!"}
                return make_response(jsonify(responseObject), 250)

            if len(password) < 4:
                responseObject = {"status": "fail", "message": "Password must be at least 4 characters long!"}
                return make_response(jsonify(responseObject), 204)

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
            else: 
                return make_response("Passwords do not match", 202)
        else: 
            return make_response("Use POST", 200)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                responseObject = {"status": "fail", "message": "Missing data!"}
                return make_response(jsonify(responseObject), 210)

            account = Account.query.filter_by(username=username).first()
            if not account:
                responseObject = {"status": "fail", "message": "User does not exist!"}
                return make_response(jsonify(responseObject), 211)

            if check_password_hash(account.password, password):
                token = jwt.encode(
                    {"id": account.id, "username": account.username,"admin": account.admin,
                     "exp": datetime.utcnow() + timedelta(minutes=30)},
                    app.config["SECRET_KEY"],
                )
                return make_response(jsonify({"token": token}), 201)

            responseObject = {"status": "fail", "message": "Incorrect Password!"}
            return make_response(jsonify(responseObject), 212)
        else: return make_response("Use POST", 200)

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        # logout
        return redirect(url_for("start"))
