from os import environ


class Config:

    SECRET_KEY = environ.get('SECRET_KEY')
    LANGUAGES = ['en', 'pl']
    CACHING_DISABLED = True

    ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')
    DEFAULT_USER_EMAIL = 'user@test.com'
    DEFAULT_USER_PASSWORD = 'password'

    # Behaviour config
    MAX_UPLOAD_SIZE_MB = 1024
    MIN_PASSWORD_LENGTH = 8
    CONFIRMATION_TIME = 60
    PASSWORD_CHANGE_TIME = 60

    # What will be logged
    DATABASE_DEBUG = False
    MAIL_DEBUG = False
    FLASK_DEBUG = False

    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_LOGIN')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'Social Insight'
    MAIL_SUBJECT_PREFIX = 'Social Insight - '

    # Paths
    DATABASE_LOCATION = 'db/base.db'
    UPLOADS_LOCATION = 'uploads'
    BABEL_CONFIG_LOCATION = 'frontend/babel.cfg'
    BABEL_TRANSLATIONS_LOCATION = 'frontend/translations'

    @staticmethod
    def init_app(app):
        pass


config = Config()
