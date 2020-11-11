from flask import Flask, request, session
from config import config
from flask_login import LoginManager
from flask_babel import Babel


login = LoginManager()
babel = Babel()


def create_app():
    app = Flask(__name__)

    login.init_app(app)
    babel.init_app(app)

    app.config.from_object(config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint, url_prefix='/')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


@babel.localeselector
def get_locale():
    default_lang = request.accept_languages.best_match(config.LANGUAGES)
    print(default_lang)
    return session.get('lang', default_lang)
