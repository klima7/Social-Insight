from threading import Thread

from flask import request, render_template, session, redirect, url_for, abort, flash
from flask_login import login_required, current_user

import analytics
import uploads
from db import *
from . import main
from config import config
from .forms import RenamePackForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def index_post():
    pack = Pack()

    if current_user.is_authenticated:
        pack.user = current_user

    db_session.add(pack)
    db_session.commit()

    session['packid'] = pack.id

    uploaded_file = request.files['file']
    path = uploads.get_path_for_pack(pack.id)
    uploaded_file.save(path)

    thread = Thread(target=analytics.analyse, args=[pack.id])
    thread.start()

    return "", 204


@main.route('/lang/<lang>')
def change_language(lang):
    if lang not in config.LANGUAGES:
        return abort(404)
    session['lang'] = lang
    return redirect(url_for('main.index'))


@main.route('/account/')
@login_required
def account():
    return render_template('account.html')


def get_pack(id):
    if id == 'anonymous' and not current_user.is_authenticated and session.get('packid', None) is not None:
        pack = db_session.query(Pack).filter_by(id=session.get('packid')).first()
    elif id != 'anonymous' and current_user.is_authenticated:
        pack = db_session.query(Pack).filter_by(userid=current_user.id, id=id).first()
    else:
        abort(403)

    if pack is None:
        abort(403)
    return pack


@main.route('/packs/<id>', methods=['GET', 'POST'])
def packs(id):
    pack = get_pack(id)
    form = RenamePackForm()
    if form.validate_on_submit():
        pack.name = form.name.data
        db_session.add(pack)
        db_session.commit()
    return render_template('pack.html', pack=pack, form=form)


@main.route('/packs/<id>/remove')
def remove_pack(id):
    pack = get_pack(id)
    db_session.delete(pack)
    db_session.commit()
    flash('Pack was removed')
    return redirect(url_for('main.account'))
