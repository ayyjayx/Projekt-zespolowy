from config import DevelopmentConfig
from flask_cors import CORS
from flask_migrate import Migrate
from init import create_app
from models import db
from flask_jwt_extended import JWTManager

app = create_app()

db.init_app(app)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
