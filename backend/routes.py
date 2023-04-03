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

    @app.route("/register", methods=["GET", "POST"])
    def register():
        data = request.get_json()
        username, email = data.get("username"), data.get("email")
        password = data.get("password")

        new_account = Account.query.filter_by(email=email).first()
        if not new_account:
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

    @app.route("/login", methods=["GET", "POST"])
    def login():
        auth = request.get_json()
        if not auth or not auth.get("username") or not auth.get("password"):
            responseObject = {"status": "fail", "message": "Missing data!"}
            return make_response(jsonify(responseObject), 401)

        account = Account.query.filter_by(username=auth.get("username")).first()
        if not account:
            responseObject = {"status": "fail", "message": "User does not exist!"}
            return make_response(jsonify(responseObject), 401)

        if check_password_hash(account.password, auth.get("password")):
            token = jwt.encode(
                {"id": account.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
                app.config["SECRET_KEY"],
            )

            return make_response(jsonify({"token": token}), 201)

        responseObject = {"status": "fail", "message": "Incorrect Password!"}
        return make_response(jsonify(responseObject), 403)

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        # logout
        return redirect(url_for("start"))
