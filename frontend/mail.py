from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, recipients=[to])
    msg.body = render_template('mails/' + template + '.txt', **kwargs)
    msg.html = render_template('mails/' + template + '.html', **kwargs)
    thr = Thread(target=_send_async_email, args=[app, msg])
    thr.start()
    return thr
