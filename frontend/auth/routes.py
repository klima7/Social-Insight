from .. import login
from db import *


@login.user_loader
def load_user(id):
    id = int(id)
    return db_session.query(User).filter_by(id=id).first()
