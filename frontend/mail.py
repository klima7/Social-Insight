from threading import Thread
from flask import current_app, render_template
from flask_babel import force_locale, get_locale
from flask_mail import Message
from . import mail


def _send_async_email(app, msg, lang):
    with app.app_context():
        with force_locale(lang):
            mail.send(msg)


def send_email(to, subject, template, lang=None, **kwargs):
    if lang is None:
        lang = str(get_locale())
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, recipients=[to])
    msg.html = render_template('mails/' + template + '.html', **kwargs)
    thr = Thread(target=_send_async_email, args=[app, msg, lang])
    thr.start()
    return thr
