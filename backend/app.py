import uuid

import chess
from config import DevelopmentConfig
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room
from init import create_app
from models import Game, db

app = create_app()

db.init_app(app)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins=["http://uwmchess.herokuapp.com"])
socketio.init_app(app)

CORS(
    app,
    resources={r"/*": {"origins": "http://uwmchess.herokuapp.com"}},
    headers={
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": "http://uwmchess.herokuapp.com",
    },
    supports_credentials=True,
)
jwt = JWTManager(app)
mail = Mail(app)


@socketio.on("join")
def on_join(data):  # receive user id
    user = data["user"]
    game_white = Game.query.filter_by(player_one_id=user).first()
    game_black = Game.query.filter_by(player_two_id=user).first()
    waiting_game_exists = Game.query.filter_by(player_two_id=None).first()

    if waiting_game_exists:
        if waiting_game_exists.player_one_id != user:
            room = waiting_game_exists.id
            print(f"client {user} wants to join: {room}")
            join_room(room)
            socketio.emit("newgame", room, room=room)
        else:
            print("waiting for player2")
            socketio.emit("waiting")
    else:
        if game_white:
            if game_white.result:
                if game_black:
                    if game_black.result:
                        room = str(uuid.uuid4().hex)
                    else:
                        room = game_black.id
                else:
                    room = str(uuid.uuid4().hex)
            else:
                room = game_white.id
            print(f"client {user} wants to join: {room}")
            join_room(room)
            socketio.emit("newgame", room, room=room)
        else:
            if game_black:
                if game_black.result:
                    room = str(uuid.uuid4().hex)
                else:
                    room = game_black.id
            else:
                room = str(uuid.uuid4().hex)
            print(f"client {user} wants to join: {room}")
            join_room(room)
            socketio.emit("newgame", room, room=room)
        socketio.emit("waiting")


@socketio.on("get_position")  # get replacement
def get_position(data):
    room = data["room"]
    playerId = data["playerId"]
    game = Game.query.filter_by(id=room).first()
    is_white = game.player_one_id == playerId
    if is_white:
        response = {"fen": game.fen, "color": "w"}
        emit("FENandColor", response)
    else:
        response = {"fen": game.fen, "color": "b"}
        emit("FENandColor", response)


@socketio.on("newgame_pvp")
def newgame_pvp(data):
    room = data["room"]
    playerId = data["playerId"]
    current_game = Game.query.filter_by(id=room).first()
    if current_game and not current_game.result:
        if current_game.player_one_id != playerId:
            if current_game.player_two_id:
                response = {"id": current_game.id}
                emit("redirect_to_game", response)
            else:
                current_game.set_player_black(playerId)
                current_game.save()
                response = {
                    "id": current_game.id,
                    "white": current_game.player_one_id,
                    "black": current_game.player_two_id,
                }
                emit("redirect_to_game", response, broadcast=True)
        elif current_game.player_two_id:
            response = {
                "id": current_game.id,
                "white": current_game.player_one_id,
                "black": current_game.player_two_id,
            }
            emit("redirect_to_game", response)
        else:
            emit("waiting for player2", "", to=room)
    else:
        board = chess.Board()
        new_game = Game(id=room, fen=board.fen(), player_one_id=playerId)
        new_game.save()
        response = {"id": new_game.id, "white": new_game.player_one_id, "black": ""}
        emit("waiting for player2", response, to=room)


@socketio.on("game_pvp")
def game_pvp(data):
    room = data["room"]
    game = Game.query.filter_by(id=room).first()
    fen = game.fen
    board = chess.Board()
    board.set_fen(fen)
    move = data["move"]
    if move:
        game.add_move(board.san(chess.Move.from_uci(move)))
        if chess.Move.from_uci(move) in board.legal_moves:
            try:
                board.push(board.parse_uci(move))
                fen = board.fen()
                game.update_fen(fen)
                if board.is_game_over():
                    if board.result() == "1-0":
                        result = "WHITE WON"
                    elif board.result() == "0-1":
                        result = "BLACK WON"
                    else:
                        result = "DRAW"
                    game.set_result(outcome=result)
                    game.set_end_time()
                game.save()
            except ValueError:
                response = {"move": "illegal"}
                emit("response", response, status=201)
        #    response = {"move": "legal"}
        #    emit('response', response, status=200)
    response = game.fen
    print(game.fen)
    emit("fenResponse", response, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
