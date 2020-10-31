from flask import session, render_template
from . import api
from db import *


def _check_ready():
    id = session.get('packid', None)
    if not id:
        return False
    pack = db_session.query(Pack).filter_by(id=id).one_or_none()
    if not pack:
        return False
    return pack.done


@api.route("/packs/anonymous/ready")
def check_ready():
    done = _check_ready()
    return {"done": done}


@api.route("/packs/anonymous/graphs")
def get_graphs():
    if not _check_ready():
        return 404

    id = session.get('packid', None)
    pack = db_session.query(Pack).filter_by(id=id).one_or_none()

    return render_template("graphs.html", pack=pack)
