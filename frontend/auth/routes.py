from frontend.util import display_errors_with_flash
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from db import *
from . import auth
from .forms import LoginForm, RegisterForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login success!', 'success')
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.account')
            return redirect(next)
        flash('Invalid login or password', 'error')
        return render_template('login.html', form=form)
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
        flash('Register success!', 'success')
        return redirect(url_for('auth.login'))
    display_errors_with_flash(form)
    return render_template('register.html', form=form)
