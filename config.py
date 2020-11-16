from os import environ


class Config:
    MAX_UPLOAD_SIZE_MB = 1024
    DATABASE_LOGGING = False    # True jeśli chcemy by wyświetlały się w konsoli wszystkie tworzone zapytania
    LANGUAGES = ['en', 'pl']
    CACHING_DISABLED = True     # Konieczne, aby wszyskie zmiany w plikach css i js były uwzględniane przez przeglądarkę

    MIN_PASSWORD_LENGTH = 8

    DATABASE_LOCATION = 'db/base.db'
    UPLOADS_LOCATION = 'uploads'
    BABEL_CONFIG_LOCATION = 'frontend/babel.cfg'
    BABEL_TRANSLATIONS_LOCATION = 'frontend/translations'

    SECRET_KEY = environ.get('SECRET_KEY')


config = Config()
