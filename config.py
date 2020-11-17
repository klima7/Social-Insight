from os import environ


class Config:
    MAX_UPLOAD_SIZE_MB = 1024
    DATABASE_LOGGING = False
    LANGUAGES = ['en', 'pl']
    CACHING_DISABLED = True
    SECRET_KEY = environ.get('SECRET_KEY')

    MIN_PASSWORD_LENGTH = 8

    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_LOGIN')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEBUG = False
    MAIL_DEFAULT_SENDER = 'Social Insight'
    MAIL_SUBJECT_PREFIX = 'Social Insight - '

    # Paths
    DATABASE_LOCATION = 'db/base.db'
    UPLOADS_LOCATION = 'uploads'
    BABEL_CONFIG_LOCATION = 'frontend/babel.cfg'
    BABEL_TRANSLATIONS_LOCATION = 'frontend/translations'


config = Config()
