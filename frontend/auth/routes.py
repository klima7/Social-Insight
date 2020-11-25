from frontend.util import display_errors_with_flash
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from frontend.mail import send_email
from db import *
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ResetPasswordEmailForm, ResetPasswordForm


@auth.after_app_request
def after_request(response):
    if request.endpoint != 'static' and request.endpoint != 'auth.login':
        session['prev'] = request.endpoint
    return response


def add_anonymous_pack_to_user(user):
    pack_id = session.get('packid', None)
    if pack_id is not None:
        pack = db_session.query(Pack).filter_by(id=pack_id).first()
        if pack is not None and pack.userid is None:
            pack.userid = user.id
            db_session.add(pack)
            db_session.commit()
            return True
    return False


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter_by(email=form.email.data).first()

        # Niepotwierdzony mail
        if user is not None and not user.confirmed and session.get('prev') != 'auth.confirm':
            session['email'] = form.email.data
            url = url_for('auth.resend')
            flash(f'Please confirm this email first! Click <a href="{url}">here</a> to resend confirmation', 'warning')
            return render_template('login.html', form=form)

        # Poprawne logowanie
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login success!', 'success')

            if add_anonymous_pack_to_user(user):
                flash('New pack was added to your account!', 'success')

            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.account')
            return redirect(next)

        # Niepoprawne dane do logowania
        flash('Invalid login or password', 'error')
        return render_template('login.html', form=form)

    # Wyświetlenie formularza
    display_errors_with_flash(form)
    return render_template('login.html', form=form)


@auth.route('/logout/')
def logout():
    flash('You have loged out', 'success')
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), password=form.password.data)
        db_session.add(user)
        db_session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Account Confirmation', 'confirmation', token=token)
        flash('Register success! Please confirm your email before logging', 'success')

        if add_anonymous_pack_to_user(user):
            flash('New pack was added to your account!', 'success')

        return redirect(url_for('auth.login'))
    display_errors_with_flash(form)
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('Your account is already confirmed', 'success')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db_session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired', 'warning')
    return redirect(url_for('main.index'))


@auth.route('/resend/', methods=['GET', 'POST'])
def resend():
    user = db_session.query(User).filter_by(email=session.get('email', 'unknown')).first()
    token = user.generate_confirmation_token()
    send_email(user.email, 'Account Confirmation', 'confirmation', user=user, token=token)
    flash('Email confirmation was sent again', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/change-password/', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.current_password.data):
            current_user.password = form.new_password.data
            db_session.add(current_user)
            db_session.commit()
            flash('Password changed', 'success')
            return redirect(url_for('main.account'))
        else:
            flash('Current password is invalid!', 'error')
    display_errors_with_flash(form)
    return render_template('change_password.html', form=form)


@auth.route('/reset-password-request/', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordEmailForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Password', 'reset_password', token=token)
            flash('Email with instructions to reset password was sent', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('This email address is not registered!', 'error')
    display_errors_with_flash(form)
    return render_template('reset_password_request.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db_session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('The reset link is invalid or has expired', 'warning')
            return redirect(url_for('main.index'))
    display_errors_with_flash(form)
    return render_template('reset_password.html', form=form)


@auth.route('/remove-account/confirm')
@login_required
def remove_account_confirm():
    address = url_for('auth.remove_account')
    flash(f'Are you sure that you want to delete this account? <a href="{address}">Yes</a>', 'error')
    return redirect(url_for('main.account'))


@auth.route('/remove-account/proceed')
@login_required
def remove_account():
    db_session.delete(current_user)
    db_session.commit()
    flash('Your account was removed', 'success')
    return redirect(url_for('main.index'))
