from time import time_ns
from flask import Flask, request, session
from flask_login import LoginManager
from flask_babel import Babel
from lorem_text import lorem
from flask_bootstrap import Bootstrap
from db import *


login = LoginManager()
babel = Babel()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    login.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)

    app.config.from_object(config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint, url_prefix='/')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    add_jinja_commands(app)

    return app


@babel.localeselector
def get_locale():
    default_lang = request.accept_languages.best_match(config.LANGUAGES)
    print(default_lang)
    return session.get('lang', default_lang)


@login.user_loader
def load_user(id):
    id = int(id)
    return db_session.query(User).filter_by(id=id).first()


def cache_suffix():
    if not config.CACHING_DISABLED:
        return ''
    return str(time_ns())


def add_jinja_commands(app):
    app.jinja_env.globals.update(cache_suffix=cache_suffix, lorem=lorem)

