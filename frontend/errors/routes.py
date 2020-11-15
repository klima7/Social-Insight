from flask import request, render_template, session, redirect, url_for, abort
from . import errors


@errors.app_errorhandler(403)
def forbidden(e):
    return render_template('error.html', title='Error 403', description='You are not authorized to access this page'), 403


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Error 404', description='Unable to find page'), 403


@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', title='Error 500', description='Internal error occured'), 500
