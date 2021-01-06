import logging

from frontend.util import cache_suffix, get_current_user, is_pygal_chart, is_pandas_table, translate_pandas_table, is_dark_mode, render_graph_png_inline
from db import *

from flask import Flask, request, session
from flask_login import LoginManager
from flask_babel import Babel, get_locale
from lorem_text import lorem
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment


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

    if not config.FLASK_DEBUG:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint, url_prefix='/')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    app.jinja_env.globals.update(cache_suffix=cache_suffix, lorem=lorem, user=get_current_user, is_dark_mode=is_dark_mode,
                                 is_pygal_chart=is_pygal_chart, is_pandas_table=is_pandas_table, translate_pandas_table=translate_pandas_table,
                                 get_locale=get_locale, Global=Global, render_graph_png_inline=render_graph_png_inline)

    return app


@babel.localeselector
def get_locale():
    default_lang = request.accept_languages.best_match(config.LANGUAGES)
    lang = session.get('lang', default_lang)
    return lang

