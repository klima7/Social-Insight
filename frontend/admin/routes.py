from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from flask_babel import _
from sqlalchemy import desc

from config import config
from db import *
from frontend.mail import send_email
from . import admin
from .forms import ReplyForm


@admin.route('/')
@login_required
def panel():
    if not current_user.is_admin():
        abort(403)
    messages_count = db_session.query(Message).count()
    users_count = db_session.query(User).count()
    return render_template('admin.html', messages_count=messages_count, users_count=users_count)


@admin.route('/messages/')
@login_required
def messages():
    if not current_user.is_admin():
        abort(403)
    messages = db_session.query(Message).order_by(desc(Message.date)).all()
    return render_template('admin_messages.html', messages=messages)


@admin.route('/messages/remove/<id>')
@login_required
def message_remove(id):
    if not current_user.is_admin():
        abort(403)
    message = db_session.query(Message).filter_by(id=id).first()
    if message is not None:
        db_session.delete(message)
        db_session.commit()
    return redirect(url_for('admin.messages'))


@admin.route('/messages/reply/<id>', methods=['GET', 'POST'])
@login_required
def message_reply(id):
    if not current_user.is_admin():
        abort(403)
    message = db_session.query(Message).filter_by(id=id).first()
    if message is None:
        return redirect(url_for('admin.messages'))

    form = ReplyForm()
    if form.validate_on_submit():
        send_email(message.sender, 'Reply', 'reply', message=message, response=form.response.data)
        flash(_('Response was sent'), 'success')
        db_session.delete(message)
        db_session.commit()
        return redirect(url_for('admin.messages'))

    return render_template('admin_reply.html', message=message, form=form)


@admin.route('/users/')
@login_required
def users():
    if not current_user.is_admin():
        abort(403)
    users = db_session.query(User).order_by(desc(User.registration_data)).all()
    return render_template('admin_users.html', users=users)


@admin.route('/users/remove/<id>')
@login_required
def user_remove(id):
    if not current_user.is_admin():
        abort(403)
    user = db_session.query(User).filter_by(id=id).first()
    if user is not None:
        db_session.delete(user)
        db_session.commit()
        flash(_('User was removed'), 'success')
    return redirect(url_for('admin.users'))


@admin.route('/users/confirm/<id>')
@login_required
def user_confirm(id):
    if not current_user.is_admin():
        abort(403)
    user = db_session.query(User).filter_by(id=id).first()
    if user is not None:
        user.confirmed = True
        db_session.add(user)
        db_session.commit()
        flash(_('User account confirmed'), 'success')
    return redirect(url_for('admin.users'))
