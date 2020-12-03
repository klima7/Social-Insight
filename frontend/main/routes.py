from threading import Thread

from flask import request, render_template, session, redirect, url_for, abort, flash, jsonify
from flask_login import login_required, current_user

import analytics
import uploads
from db import *
from . import main
from config import config
from .forms import RenamePackForm, RenameCollationForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def index_post():
    pack = Pack(status=Pack.STATUS_PENDING)

    if current_user.is_authenticated:
        pack.user = current_user

    db_session.add(pack)
    db_session.commit()

    session['packid'] = pack.id
    session.modified = True

    uploaded_file = request.files['file']
    path = uploads.get_path_for_pack(pack.id)
    uploaded_file.save(path)

    thread = Thread(target=analytics.analyse, args=[pack.id])
    thread.start()

    print('check 5')
    return jsonify({'id': pack.id})


@main.route('/lang/<lang>')
def change_language(lang):
    if lang not in config.LANGUAGES:
        return abort(404)
    session['lang'] = lang
    return redirect(session.get('prev_url', url_for('main.index')))


@main.route('/account/')
@login_required
def account():
    return render_template('account.html')


def get_pack(id):
    pack = db_session.query(Pack).filter_by(id=id).first()
    if current_user.is_authenticated and pack.userid == current_user.id or pack.id == session.get('packid', None):
        return pack
    abort(403)


@main.route('/packs/<id>', methods=['GET', 'POST'])
def packs(id):
    pack = get_pack(id)
    form = RenamePackForm()
    if form.validate_on_submit():
        pack.name = form.name.data
        flash('Pack name changed to ' + pack.name, 'success')
        db_session.add(pack)
        db_session.commit()
    return render_template('pack.html', pack=pack, form=form)


@main.route('/packs/<id>/remove/confirm')
def remove_pack_confirm(id):
    get_pack(id)
    address = url_for('main.remove_pack', id=id)
    flash(f'Are you sure that you want to remove this pack? <a href="{address}">Yes</a>', 'warning')
    return redirect(url_for('main.packs', id=id))


@main.route('/packs/<id>/remove')
def remove_pack(id):
    pack = get_pack(id)
    db_session.delete(pack)
    db_session.commit()
    flash('Pack was removed', 'success')
    return redirect(url_for('main.account'))


@main.route('/collations/create')
@login_required
def create_collation():
    collation = Collation()
    collation.user = current_user
    db_session.add(collation)
    db_session.commit()
    flash('New collation was created', 'success')
    return redirect(url_for('main.account'))


def get_collation(id):
    collation = db_session.query(Collation).filter_by(userid=current_user.id, id=id).first()
    if collation is None:
        abort(403)
    return collation


@main.route('/collations/<id>', methods=['GET', 'POST'])
@login_required
def collation(id):
    collation = get_collation(id)
    form = RenameCollationForm()
    if form.validate_on_submit():
        collation.name = form.name.data
        flash('Collation name changed to ' + collation.name, 'success')
        db_session.add(collation)
        db_session.commit()
    return render_template('collation.html', collation=collation, form=form)


@main.route('/collations/<id>/remove/confirm')
def remove_collation_confirm(id):
    get_collation(id)
    address = url_for('main.remove_collation', id=id)
    flash(f'Are you sure that you want to remove this collation? <a href="{address}">Yes</a>', 'warning')
    return redirect(url_for('main.collation', id=id))


@main.route('/collations/<id>/remove')
def remove_collation(id):
    collation = get_collation(id)
    db_session.delete(collation)
    db_session.commit()
    flash('collation was removed', 'success')
    return redirect(url_for('main.account'))


@main.route('/packs/<id>/<category>', methods=['GET', 'POST'])
def graphs_category(id, category):
    pack = get_pack(id)
    form = RenamePackForm()

    if form.validate_on_submit():
        pack.name = form.name.data
        flash('Pack name changed to ' + pack.name, 'success')
        db_session.add(pack)
        db_session.commit()

    graphs = pack.graphs.filter(Graph.category == category).order_by(Graph.id).all()
    return render_template('graphs_category.html', pack=pack, graphs=graphs, form=form, category=category)


@main.route('/packs/waiting/<packid>')
def waiting(packid):
    return render_template('waiting.html', packid=packid)


@main.route('/credits')
def credits():
    return render_template('credits.html')


@main.route('/graphs/<id>')
def graphs(id):
    graph = db_session.query(Graph).filter_by(id=id).first()
    if graph is None:
        abort(404)
    if not graph.public and not graph.pack.user == current_user:
        abort(403)
    return render_template('graph.html', graph=graph)



