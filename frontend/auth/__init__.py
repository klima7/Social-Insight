from db import *
from flask import Blueprint
from frontend import login

auth = Blueprint('auth', __name__)

from . import routes


@login.user_loader
def load_user(id):
    id = int(id)
    return db_session.query(User).filter_by(id=id).first()


login.login_view = "auth.login"
login.login_message = "Please log in to access this page"
login.login_message_category = "message"
