from os import environ


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    MAX_UPLOAD_SIZE_MB = 1024
    DATABASE_LOCATION = 'db/base.db'
    UPLOADS_LOCATION = 'uploads'
    DATABASE_LOGGING = False


config = Config()
