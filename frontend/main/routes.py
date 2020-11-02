from threading import Thread

from flask import request, render_template
from flask import session as flask_session

import analytics
import uploads
from db import *
from . import main


@main.route('/')
def index_get():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def index_post():
    pack = Pack(done=False)

    db_session.add(pack)
    db_session.commit()

    flask_session['packid'] = pack.id

    uploaded_file = request.files['file']
    path = uploads.get_path_for_pack(pack.id)
    uploaded_file.save(path)

    thread = Thread(target=analytics.analyse, args=[pack.id])
    thread.start()

    return "", 204


