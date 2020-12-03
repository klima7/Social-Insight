from flask import session, render_template
from flask_login import current_user
from . import api
from db import *


def _get_pack_status(packid):
    pack = db_session.query(Pack).filter_by(id=packid).one_or_none()
    if not pack:
        return Pack.STATUS_FAILURE
    return pack.status


@api.route("/packs/<packid>/status")
def get_pack_status(packid):
    status = _get_pack_status(packid)
    return {"status": status}


@api.route('/graphs/<id>/public')
def public_graph(id):
    graph = db_session.query(Graph).filter_by(id=id).first()
    if graph.pack.user != current_user:
        return {}, 403
    if graph is None:
        return {}, 404
    graph.public = True
    db_session.add(graph)
    db_session.commit()
    return {"public": graph.public}


@api.route('/graphs/<id>/private')
def private_graph(id):
    graph = db_session.query(Graph).filter_by(id=id).first()
    if graph.pack.user != current_user:
        return {}, 403
    if graph is None:
        return {}, 404
    graph.public = False
    db_session.add(graph)
    db_session.commit()
    return {"public": graph.public}

