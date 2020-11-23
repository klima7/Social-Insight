from flask import session, render_template
from . import api
from db import *


def _get_pack_status():
    id = session.get('packid', None)
    if not id:
        return PackStatus.FAILURE
    pack = db_session.query(Pack).filter_by(id=id).one_or_none()
    if not pack:
        return PackStatus.FAILURE
    return pack.status


@api.route("/packs/anonymous/status")
def get_pack_status():
    status = _get_pack_status()
    return {"status": status}


@api.route("/packs/anonymous/graphs")
def get_graphs():
    if not _get_pack_status():
        return 404

    id = session.get('packid', None)
    pack = db_session.query(Pack).filter_by(id=id).one_or_none()

    return render_template("graphs.html", pack=pack)
