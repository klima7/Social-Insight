import base64
import os
import tempfile
import pygal
import pandas

from flask import flash
from flask_login import current_user
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


def get_current_user():
    return current_user


def is_pygal_chart(obj):
    return isinstance(obj, pygal.graph.graph.Graph)


def is_pandas_table(obj):
    return isinstance(obj, pandas.core.frame.DataFrame)


def translate_pandas_table(table):
    return table.rename(columns=str)


def pygal2base64(chart):
    # base = tempfile.mkdtemp()
    # path_svg = os.path.join(base, 'graph.svg')
    # path_png = os.path.join(base, 'graph.png')
    # chart.render_to_file(path_svg)
    #
    # with open(path_svg) as f:
    #     content = f.read()
    #
    # svg2png(bytestring=content, write_to=path_png)
    #
    # with open(path_png, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    #     print(encoded_string)
    #     return encoded_string
    pass
