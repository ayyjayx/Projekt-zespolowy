from datetime import timedelta


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "some_dev_key"
    JWT_SECRET_KEY = "super-secret"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_COOKIE_SECURE = False
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_CSRF_PROTECT = True
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'b0f5148942a087'
    MAIL_PASSWORD = '85ae025f392454'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    JWT_SECRET_KEY = "super-secret"
    JWT_TOKEN_LOCATION = "cookies"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    SERVER_NAME = 'localhost:5000'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:projekt1234@database:5432/postgres"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_BINDS = {"temporary": "sqlite:///:memory:"}
