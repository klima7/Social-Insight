from flask import session, request
from flask_login import current_user
from sqlalchemy.exc import InvalidRequestError

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


@api.route('/collations/<collation_id>', methods=['POST'])
def collations_post(collation_id):
    graph_id = request.json['id']
    graph = db_session.query(Graph).filter_by(id=graph_id).first()
    collation = db_session.query(Collation).filter_by(id=collation_id).first()
    if graph is None or collation is None:
        return {}, 404
    if graph.pack.user != current_user or collation.user != current_user:
        return {}, 403
    graph.collations.append(collation)
    db_session.add(graph)
    db_session.commit()
    return {"present": True}


@api.route('/collations/<collation_id>', methods=['DELETE'])
def collations_delete(collation_id):
    graph_id = request.json['id']
    graph = db_session.query(Graph).filter_by(id=graph_id).first()
    collation = db_session.query(Collation).filter_by(id=collation_id).first()
    if graph is None or collation is None:
        return {}, 404
    if graph.pack.user != current_user or collation.user != current_user:
        return {}, 403
    try:
        graph.collations.remove(collation)
        db_session.add(graph)
        db_session.commit()
    except ValueError:
        pass
    return {"present": False}


@api.route('/christmas', methods=['POST'])
def christmas_post():
    status = request.json['status']
    g = db_session.query(Global).first()
    g.christmas_event = status
    db_session.add(g)
    db_session.commit()
    return {"status": g.christmas_event}


@api.route('/files/<file_id>/progress')
def file_progress(file_id):
    file = db_session.query(File).filter_by(id=file_id).first()

    progress = 0
    ready = False

    if file is not None:
        progress = file.progress
        ready = file.ready

    return {'progress': progress, 'ready': ready}
