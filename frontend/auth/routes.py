from frontend.util import display_errors_with_flash
from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import LoginForm, RegisterForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login success!', 'success')
        return redirect(url_for('main.index'))
    display_errors_with_flash(form)
    return render_template('login.html', form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Register success!', 'success')
        return redirect(url_for('main.index'))
    display_errors_with_flash(form)
    return render_template('register.html', form=form)
