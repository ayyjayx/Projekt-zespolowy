from init import create_app
from models import db
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_cors import CORS

app = create_app()

db.init_app(app)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0")