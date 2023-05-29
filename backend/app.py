from config import DevelopmentConfig
from flask_cors import CORS
from flask_migrate import Migrate
from init import create_app
from models import db, Game
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, join_room, emit
from flask_mail import Mail
import chess
import uuid

app = create_app()

db.init_app(app)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000"])
socketio.init_app(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, 
     headers={'Access-Control-Allow-Credentials': 'true', 
              'Access-Control-Allow-Origin': 'http://localhost:3000'}, 
     supports_credentials=True)
jwt = JWTManager(app)
mail = Mail(app)

@socketio.on("join")
def on_join(data): # recieve user id
     user = data["user"]
     room = str(uuid.uuid4().hex)
     print(f"client {user} wants to join: {room}")
     join_room(room)
     socketio.emit("newgame", room, room=room)

@socketio.on("waiting_room")
def wait(room):
     ids = {} # ??? jak dodać id obu???
     if len(socketio.rooms[room]) == 2: # idk czy to działa
          emit("redirect_to_game", room, ids)

@socketio.on("get_position") # get replacement
def get_position(room):
     game = Game.query.filter_by(id=room).first()
     emit("FEN", game.fen)

@socketio.on('newgame_pvp')
def newgame_pvp(data):
     print(f"newgame_pvp data: {data}")
     room = data['room']
     white = data['white']
     black = data['black']

     current_game = Game.query.filter_by(id=room).first()
     if current_game and not current_game.result:
          response = {"id": current_game.id}
          emit("not_auth", response)
     else:
          board = chess.Board()
          new_game = Game(
               id = room,
               fen = board.fen(),
               player_one_id = white,
               player_two_id = black
          )
          new_game.save()
          response = {"id": new_game.id}
          emit('new game', response, to=room)

@socketio.on("game_pvp")
def game_pvp(data):
     room = data['room']
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
                    emit('response', response, status=201)
               response = {"move": "legal"}
               emit('response', response, status=200)
     response = {"FEN": fen}
     emit('response', response, status=203)

if __name__ == "__main__":
    socketio.run(app)
