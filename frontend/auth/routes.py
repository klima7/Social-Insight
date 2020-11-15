from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import LoginForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Logging success")
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)
