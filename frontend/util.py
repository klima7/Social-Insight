from flask import flash
from config import config
from time import time_ns


def cache_suffix():
    if not config.CACHING_DISABLED:
        return ''
    return str(time_ns())


def display_errors_with_flash(form):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            flash(err, 'error')
