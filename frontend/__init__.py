from frontend.util import cache_suffix
from flask import Flask, request, session
from flask_login import LoginManager
from flask_babel import Babel
from lorem_text import lorem
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from db import *


login = LoginManager()
babel = Babel()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    login.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    config.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint, url_prefix='/')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    app.jinja_env.globals.update(cache_suffix=cache_suffix, lorem=lorem, GraphName=GraphName)

    return app


@babel.localeselector
def get_locale():
    default_lang = request.accept_languages.best_match(config.LANGUAGES)
    print(default_lang)
    return session.get('lang', default_lang)

