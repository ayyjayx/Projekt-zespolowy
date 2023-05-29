from datetime import datetime, timedelta

from config import Config
from flask import jsonify, make_response, render_template_string, request
from flask_cors import cross_origin
from flask_jwt_extended import (create_access_token, create_refresh_token,get_jwt_identity,
                                jwt_required, unset_jwt_cookies, set_access_cookies,
                                set_refresh_cookies)
from flask_mail import Mail, Message
from models import Account, ResetToken, Game
# from flask_socketio import SocketIO, emit, join_room
import chess
import uuid

def init_routes(app):

    @app.route("/creategame", methods=["POST", "GET"]) # create a new game for logged-in user
    @jwt_required()
    def newgame_auth():
        current_user = get_jwt_identity()
        current_game = Game.query.filter_by(player_one_id=current_user).first()

        if current_game and not current_game.result:
            response = {"id": current_game.id}
            return make_response(jsonify(response), 200)
        else:
            board = chess.Board()
            new_game = Game(
                id = str(uuid.uuid4().hex),
                fen = board.fen(),
                player_one_id = current_user
            )
            new_game.save()
            response = {"id": new_game.id}
            return make_response(jsonify(response), 200)
    
    @app.route("/game", methods=["POST", "GET"]) # validate and save moves for logged-in user
    @jwt_required()
    def game():
        current_user = get_jwt_identity()
        game_id = request.args.get("gameId")
        game = Game.query.filter_by(id=game_id).first()

        if current_user != (game.player_one_id or game.player_two_id):
            response = {"game": "Authorization denied"}
            return make_response(jsonify(response), 201)
        
        fen = game.fen    
        board = chess.Board()
        board.set_fen(fen)

        if request.method == "GET":
            response = {"FEN": fen}
            return make_response(jsonify(response), 200)

        data = request.get_json()
        move = data.get("move")
        reverse = data.get("reverse")

        if reverse:
            try:
                board.pop()
                fen = board.fen()
                game.update_fen(fen)
                game.save()
            except ValueError:
                response = {"move": "Cannot reverse this move"}
                return make_response(jsonify(response), 201)
            response = {"move": "Successfully reversed"}
            return make_response(jsonify(response), 200)
        
        if move:
            game.add_move(board.san(chess.Move.from_uci(move)))
            print(board.san(chess.Move.from_uci(move)))
            if chess.Move.from_uci(move) in board.legal_moves:
                try:
                    board.push(board.parse_uci(move))

                    fen = board.fen()
                    game.update_fen(fen)

                    if board.is_game_over():
                        if board.result() == '1-0':
                            result = "WHITE WON"
                        elif board.result() == '0-1':
                            result = "BLACK WON"
                        else:
                            result = "DRAW"

                        game.set_result(outcome=result)
                        game.set_end_time()

                    game.save()

                except ValueError:
                    response = {"move": "illegal"}
                    return make_response(jsonify(response), 201)
                response = {"move": "legal"}
                return make_response(jsonify(response), 200)
        
        response = {"FEN": fen}
        return make_response(jsonify(response), 203)

    @app.route("/game_noauth", methods=["POST", "GET"]) # validate and save game for not-auth user
    def game_noauth():
        data = request.get_json()
        fen = data.get("fen")   
        board = chess.Board()
        board.set_fen(fen)

        data = request.get_json()
        move = data.get("move") # in uci
        reverse = data.get("reverse")
        moveObj = chess.Move.from_uci(move)

        if reverse:
            try:
                board.pop()
                fen = board.fen()
            except ValueError:
                response = {"move": "Cannot reverse this move", "fen": fen}
                return make_response(jsonify(response), 201)
            response = {"move": "reversed", "fen": fen}
            return make_response(jsonify(response), 200)
        
        elif moveObj in board.legal_moves:
            try:
                board.push(board.parse_uci(move))
                fen = board.fen()
            except ValueError:
                response = {"move": "illegal", "fen": fen}
                return make_response(jsonify(response), 201)
            response = {"move":"legal", "fen": fen}
            return make_response(jsonify(response), 200)
        
        response = {"fen": fen}
        return make_response(jsonify(response), 203)
        
    @app.route("/profile/games", methods=["GET"]) # show player's previous and ongoing games
    @jwt_required()
    def mygames():
        current_user = get_jwt_identity()
        games = Game.query.filter_by(player_one_id=current_user).all() # W
        games2 = Game.query.filter_by(player_two_id=current_user).all() # B
        games += games2
        games_dict = [game.to_dict() for game in games]
        response = {"games": games_dict}
        return make_response(jsonify(response), 200)

    @app.route("/loggedhome", methods=["GET", "POST"])
    def home():
        response = {"status":"ok"}
        return make_response(jsonify(response), 200)

    @app.route("/registration", methods=["GET", "POST"])
    def registration():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            passwordRepeat = data.get("passwordRepeat")

            if not username or not password or not email or not passwordRepeat:
                response = {"registration": "Missing data"}
                return make_response(jsonify(response), 202)

            if len(password) < 4:
                response = {"registration": "Password must be >=4 characters long"}
                return make_response(jsonify(response), 202)

            if password == passwordRepeat:
                username_exists = Account.query.filter_by(username=username).first()
                email_exists = Account.query.filter_by(email=email).first()
                if not username_exists:
                    if not email_exists:
                        new_account = Account(username=username, email=email)
                        new_account.set_password(password)
                        new_account.save()
                        response = {"registration": "Successfully registered"}
                        return make_response(jsonify(response), 200)
                    else:
                        response = {"registration": "Ten email jest już przypisany do konta"}
                        return make_response(jsonify(response), 202)
                else:
                    response = {"registration": "Account already exists."}
                    return make_response(jsonify(response), 202)
            else:
                response = {"registration": "Passwords do not match"}
                return make_response(jsonify(response), 202)
        else:
            response = {"registration": "Use POST method"}
            return make_response(jsonify(response), 200)

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            response = {"login": "Missing data"}
            return make_response(jsonify(response), 201)

        account = Account.query.filter_by(username=username).first()

        if not account:
            response = {"login": "Account does not exist"}
            return make_response(jsonify(response), 201)

        if account.check_password(password):
            access_token = create_access_token(identity=account.id)
            refresh_token = create_refresh_token(identity=account.id)
            response = jsonify(
                access_token=access_token, refresh_token=refresh_token
            )
            response = jsonify({"login": "Successful"})
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
                
            return make_response(response, 200)

        response = {"login": "Incorrect Password"}
        return make_response(jsonify(response), 201)

    @app.route("/logout", methods=["POST"])
    def logout():
        response = jsonify({"logout": "Successful"})
        unset_jwt_cookies(response)
        return make_response(response, 200)

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def show_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)
        
        if not account:
            response = {"profile": "Account does not exist"}
            return make_response(jsonify(response), 404)

        response = {
                    "id": account.id,
                    "email": account.email,
                    "username": account.username,
                    "created_on": account.created_on,
                    }
        return make_response(jsonify(response), 200)

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
            response = {"profile": "Account does not exist"}
            return make_response(jsonify(response), 201)

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
                        response = {"profile": "Username already in use"}
                        return make_response(jsonify(response), 201)

                if new_email != "":
                    email_exists = Account.query.filter_by(email=new_email).first()
                    if not email_exists:
                        account.update_email(new_email)
                    else:
                        response = {"profile": "Email already in use"}
                        return make_response(jsonify(response), 201)

                account.save()
                response = {"profile": "Successfully updated"}
                return make_response(jsonify(response), 200)

            response = {"profile": "Wrong password"}
            return make_response(jsonify(response), 201)

        else:
            response = {"id": account.id, "email": account.email, "username": account.username}
            return make_response(jsonify(response), 200)

    @app.route("/profile/delete", methods=["DELETE"])
    @jwt_required()
    @cross_origin(supports_credentials=True)
    def delete_account():
        current_user = get_jwt_identity()
        account = Account.query.get(current_user)

        if not account:
            response = {"delete": "Account does not exist"}
            return make_response(jsonify(response), 404)

        account.delete()

        response = {"delete": "Account successfully deleted"}
        return make_response(jsonify(response), 200)

    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        response = jsonify({'refresh': True})
        set_access_cookies(response, access_token)
        return make_response(response, 200)

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
            response = {"email": "Email has been sent"}
            return make_response(jsonify(response), 200)

        except Exception as e:
            response = {"email": "Could not send email", "exception": f"{str(e)}"}
            return make_response(jsonify(response), 201)

    @app.route("/reset_password", methods=["GET", "POST"])
    @cross_origin()
    def reset_password():
        token = None

        if request.method == "GET":
            token = request.args.get("token")
            email = request.args.get("email")
            response = {"reset": "Successfully passed url params"}
            return make_response(jsonify(response), 200)

        if request.method == "POST":
            data = request.get_json()
            token = data.get('token')
            email = data.get('email')
            
            reset_token = ResetToken.query.filter_by(token=token).first()

            expiration_time = timedelta(hours=1)
            current_time = datetime.utcnow()

            if reset_token:
                reset_token.delete()
            else:
                response = {"reset": "Access to reset link has expired"}
                return make_response(jsonify(response), 201)
            
            if current_time - reset_token.created_at > expiration_time:
                reset_token.delete()
                response = {"reset": "Reset token has expired"}
                return make_response(jsonify(response), 201)
            
            account = Account.query.filter_by(email=email).first()
            if not account:
                response = {"reset": "User does not exist"}
                return make_response(jsonify(response), 201)

            new_password = data.get("password")
            new_passwordR = data.get("passwordRepeat")

            if not new_password or not new_passwordR:
                response = {"reset": "Missing data"}
                return make_response(jsonify(response), 201)

            if len(new_password) < 4:
                response = {"reset": "Password must be at least 4 characters long"}
                return make_response(jsonify(response), 201)

            if new_password == new_passwordR:
                account.update_password(new_password)
                account.save()
                response = {"reset": "Password successfully updated"}
                return make_response(jsonify(response), 200)

            else:
                response = {"reset": "Passwords do not match"}
                return make_response(jsonify(response), 201)

    @app.route("/check_auth", methods=["GET"])
    @jwt_required()
    def checking():
        response = {"auth": True}
        return make_response(jsonify(response), 200)