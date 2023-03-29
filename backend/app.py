from init import create_app
from models import db
from flask_migrate import Migrate
from config import DevelopmentConfig

app = create_app()

db.init_app(app)
app.config.from_object(DevelopmentConfig)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0")