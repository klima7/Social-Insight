from threading import Thread

from flask import request, render_template, session, redirect, url_for, abort

import analytics
import uploads
from db import *
from . import main
from config import config


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def index_post():
    pack = Pack(done=False)

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
