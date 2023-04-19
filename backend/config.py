from datetime import timedelta

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "some_dev_key"
    JWT_SECRET_KEY = "super-secret"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = False
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'b11e69d7674e43'
    MAIL_PASSWORD = '59478b0bd8b607'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SERVER_NAME = 'localhost:5000'

    JWT_SECRET_KEY = "super-secret"
    JWT_TOKEN_LOCATION = "cookies"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:projekt1234@database:5432/postgres"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_BINDS = {
        "temporary": "sqlite:///:memory:"
    }
