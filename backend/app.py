from config import DevelopmentConfig
from flask_cors import CORS
from flask_migrate import Migrate
from init import create_app
from models import db
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = create_app()

db.init_app(app)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)

CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:3000"}},
    headers={
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": "http://localhost:3000",
    },
    supports_credentials=True,
)
jwt = JWTManager(app)
mail = Mail(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
