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


@api.route("/packs/last/status")
def get_pack_status():
    status = _get_pack_status()
    return {"status": status}
