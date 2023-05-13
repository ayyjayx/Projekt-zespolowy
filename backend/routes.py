from datetime import datetime, timedelta

from config import Config
from flask import jsonify, make_response, render_template_string, request
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, create_refresh_token,get_jwt_identity,
                                jwt_required, unset_jwt_cookies, set_access_cookies,
                                set_refresh_cookies)
from flask_mail import Mail, Message
from models import Account, ResetToken, Game
import chess
import uuid

def init_routes(app):
    @app.route("/creategameauth", methods=["POST", "GET"]) # create a new game for logged-in user
    @jwt_required()
    def newgame_auth():
        current_user = get_jwt_identity()

        board = chess.Board()
        new_game = Game(
            id = str(uuid.uuid4().hex),
            fen = board.fen(),
            player_one_id = current_user,
        )
        new_game.save()
        
        return jsonify({"id": new_game.id})
    
    @app.route("/authgame", methods=["POST"]) # validate and save moves for logged-in user
    @jwt_required()
    def game_auth():
        game_id = request.args.get("gameId")
        game = Game.query.filter_by(id=game_id).first()
        fen = game.fen    
        board = chess.Board()
        board.set_fen(fen)

        data = request.get_json()
        move = data.get("move") # in uci
        over = data.get("over")
        reverse = data.get("reverse")

        if reverse:
            try:
                board.pop()
                fen = board.fen()
                game.update_fen(fen)
                game.save()
            except ValueError:
                return jsonify({"move": "cannot reverse"})
            
            return jsonify({"move": "reversed"})

        if over:
            if move:
                try:
                    board.push(board.parse_uci(move))
                    fen = board.fen()
                    game.update_fen(fen)
                    game.save()
                except ValueError:
                    return jsonify({"move": "illegal"})
                
            if board.is_game_over():
                result = "DRAW"
            if board.is_stalemate():
                result = "STALEMATE"
            if board.is_insufficient_material():
                result = "INSUFFICIENT_MATERIAL"
            if board.is_seventyfive_moves():
                result = "SEVENTYFIVE_MOVES"
            if board.is_fivefold_repetition():
                result = "FIVEFOLD_REPETITION"
            if board.can_claim_threefold_repetition():
                result = "THREEFOLD_REPETITION"
            if board.is_checkmate():
                if board.result() == '1-0':
                    result = "WHITE WON"
                else:
                    result = "BLACK WON"

            game.set_result(outcome=result)
            game.set_end_time()
            game.save()
            return jsonify({"game":"end"})

        elif chess.Move.from_uci(move) in board.legal_moves:
            try:
                board.push(board.parse_uci(move))
                fen = board.fen()
                game.update_fen(fen)
                game.save()
            except ValueError:
                return jsonify({"move": "illegal"})
            
            return jsonify({"move":"legal"})

    @app.route("/creategame", methods=["POST", "GET"]) # create a new game for not-auth user
    def newgame():
        board = chess.Board()
        new_game = Game(
            id = str(uuid.uuid4().hex),
            fen = board.fen(),
            player_one_id = 0,
        )
        new_game.save()
        
        return jsonify({"id": new_game.id})

    @app.route("/game", methods=["POST", "GET"]) # validate and save game for not-auth user
    def game():
        game_id = request.args.get("gameId")
        game = Game.query.filter_by(id=game_id).first()
        fen = game.fen  

        if request.method == "GET": # do przywracania gry na froncie
            return jsonify({"fen": fen})

        board = chess.Board()
        board.set_fen(fen)

        data = request.get_json()
        move = data.get("move") # in uci
        over = data.get("over")
        reverse = data.get("reverse")

        if reverse:
            try:
                board.pop()
                fen = board.fen()
                game.update_fen(fen)
                game.save()
            except ValueError:
                return jsonify({"move": "cannot reverse"})
            
            return jsonify({"move": "reversed"})

        if over:
            if move:
                try:
                    board.push(board.parse_uci(move))
                    fen = board.fen()
                    game.update_fen(fen)
                    game.save()
                except ValueError:
                    return jsonify({"move": "illegal"})
                
            if board.is_game_over():
                result = "DRAW" # na razie tak, reszta przypadkow draw zawsze daje false

            if board.is_seventyfive_moves(): # = draw
                result = "SEVENTYFIVE_MOVES"
            if board.is_fivefold_repetition(): # = draw
                result = "FIVEFOLD_REPETITION"
            if board.can_claim_threefold_repetition(): # = draw
                result = "THREEFOLD_REPETITION"
            if board.is_checkmate() or board.is_stalemate():
                if board.result() == '1-0':
                    result = "WHITE WON"
                else:
                    result = "BLACK WON"

            game.set_result(outcome=result)
            game.set_end_time()
            game.save()
            return jsonify({"game":"end"})

        elif chess.Move.from_uci(move) in board.legal_moves:
            try:
                board.push(board.parse_uci(move))
                fen = board.fen()
                game.update_fen(fen)
                game.save()
            except ValueError:
                return jsonify({"move": "illegal"})
            
            return jsonify({"move":"legal"})
        
    @app.route("/profile/games", methods=["GET"]) # show player's previous and ongoing games
    @jwt_required()
    def mygames():
        current_user = get_jwt_identity()
        games = Game.query.filter_by(player_one_id=current_user).all()
        games_dict = [game.to_dict() for game in games]
        return jsonify(games_dict)

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
                response = jsonify({'login': True})
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                
                return response

            return make_response("Incorrect Password.", 200)
        else:
            return make_response("Use POST", 201)

    @app.route("/logout", methods=["POST"])
    def logout():
        response = jsonify({'logout': True})
        unset_jwt_cookies(response)
        return response

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def show_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        
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
            201,
        )

    @app.route("/profile/update", methods=["GET", "POST"])
    @jwt_required()
    @cross_origin(supports_credentials=True)
    def edit_account():
        payload = request.get_json()
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
                    username_exists = Account.query.filter_by(username=new_username).first()
                    if not username_exists:
                        account.update_username(new_username)
                    else:
                        return make_response("User already exists")

                if new_email != "":
                    email_exists = Account.query.filter_by(email=new_email).first()
                    if not email_exists:
                        account.update_email(new_email)
                    else:
                        return make_response("Email already used")

                account.save()
                response = make_response("Dane konta zaktualizowane", 200)
                return response

            return make_response("Niepoprawne hasło.", 201)

        return (
            jsonify(
                {"id": account.id, "email": account.email, "username": account.username}
            ),
            201,
        )

    @app.route("/profile/delete", methods=["DELETE"])
    @jwt_required()
    @cross_origin(supports_credentials=True)
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
        current_user = get_jwt_identity()
        # account = Account.query.get(current_user)
        access_token = create_access_token(identity=current_user)
        response = jsonify({'refresh': True})
        set_access_cookies(response, access_token)
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

    @app.route("/check_auth", methods=["GET"])
    @jwt_required()
    def checking():
        return jsonify(auth=True)