from frontend.util import display_errors_with_flash
from flask import render_template, redirect, url_for, flash, request, session, Markup
from flask_login import login_user, logout_user, login_required, current_user
from frontend.mail import send_email
from db import *
from . import auth
from .forms import LoginForm, RegisterForm, ChangePasswordForm


@auth.after_app_request
def after_request(response):
    if request.endpoint != 'static' and request.endpoint != 'auth.login':
        session['prev'] = request.endpoint
    return response


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
    return redirect(url_for('auth.login'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(), password=form.password.data)
        db_session.add(user)
        db_session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Account Confirmation', 'confirmation', user=user, token=token)
        flash('Register success! Please confirm your email before logging', 'success')
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
            flash('Password changed', 'success')
            return redirect(url_for('main.account'))
        else:
            flash('Current password is invalid!', 'error')
    display_errors_with_flash(form)
    return render_template('change_password.html', form=form)
